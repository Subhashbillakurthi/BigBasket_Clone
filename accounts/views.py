from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from .models import Address
from .models import Profile, Address
from products.models import Category
from cart.models import CartItem
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from orders.models import Order
from django.contrib import messages
from .models import EmailOTP
import random
from vendor.models import Vendor
from django.core.cache import cache
from django.utils import timezone

def login_view(request):
    LOCK_TIME = 5 * 60  # 5 minutes in seconds
    MAX_ATTEMPTS = 3

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        key_attempts = f"login_attempts_{username}"
        key_lock = f"login_locked_{username}"
        now = timezone.now().timestamp()

        # Check lock status
        locked_until = cache.get(key_lock)
        if locked_until and float(locked_until) > now:
            messages.error(request, "Too many failed attempts. Try again after 5 minutes.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.profile.s_vendor != True and user.is_staff != True:
            cache.delete(key_attempts)
            cache.delete(key_lock)
            login(request, user)
            return redirect('home')
        elif user is not None and user.profile.s_vendor == True and user.is_staff != True:
            cache.delete(key_attempts)
            cache.delete(key_lock)
            login(request, user)
            return redirect('vendor_dashboard')
        elif user is not None and user.is_staff == True:
            cache.delete(key_attempts)
            cache.delete(key_lock)
            login(request, user)
            return redirect('custom_admin_dashboard')
        else:
            attempts = cache.get(key_attempts, 0) + 1
            cache.set(key_attempts, attempts, LOCK_TIME)
            if attempts >= MAX_ATTEMPTS:
                lock_until = now + LOCK_TIME
                cache.set(key_lock, lock_until, LOCK_TIME)
                messages.error(request, "Too many failed attempts. Try again after 5 minutes.")
            else:
                messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')



def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user_type = request.POST.get("user_type")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            # Create user
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            user.save()

            # Vendor case
            if user_type == "vendor":
                user.profile.s_vendor = True
                user.profile.save()

                # ✅ Create Vendor entry
                Vendor.objects.create(
                    user=user.profile,
                    shop_name=f"{username}'s Shop",   # default shop name
                    gst_number="",                   # leave blank, update later
                    phone_number=user.profile.phone_number or "",
                )

            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")

    return render(request, "accounts/register.html")



def profile(request, username):
    try:
        user = User.objects.get(username=username)
        categories = Category.objects.all()
        return render(request, "accounts/profile.html", {"profile_user": user,"categories": categories})
    except User.DoesNotExist:
        messages.error(request, "User not found. Please register.")
        return redirect("register")
    
import secrets

def send_otp(request):
    LOCK_TIME = 5 * 60
    MAX_ATTEMPTS = 3

    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # ✅ Create new user if email not found
            user = User.objects.create_user(
                username=email,
                email=email,
                password=secrets.token_urlsafe(12),  # random safe password
            )
            user.set_unusable_password()  # make sure normal login is disabled
            user.save()

            # Also create profile for this user
            if not hasattr(user, "profile"):
                Profile.objects.create(user=user)

        # 🔒 Check if user is locked from normal login
        key_lock = f"login_locked_{user.username}"
        now = timezone.now().timestamp()
        locked_until = cache.get(key_lock)
        if locked_until and float(locked_until) > now:
            messages.error(request, "Too many failed attempts. Try again after 5 minutes.")
            return render(request, "accounts/otp.html")

        # ✅ Generate OTP
        otp = str(random.randint(100000, 999999))  
        EmailOTP.objects.update_or_create(user=user, defaults={"otp": otp})

        send_mail(
            "Your OTP Code",
            f"Your OTP is {otp}. It will expire in 5 minutes.",
            "yourgmail@gmail.com",
            [email],
        )

        request.session["otp_user_id"] = user.id
        messages.success(request, "OTP sent successfully! Please check your email.")
        return redirect("verify_otp")

    return render(request, "accounts/otp.html")




def verify_otp(request):
    LOCK_TIME = 5 * 60   # 5 minutes in seconds
    MAX_ATTEMPTS = 3

    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        user_id = request.session.get("otp_user_id")
        if not user_id:
            return redirect("send_otp")
        user = User.objects.get(id=user_id)
        otp_record = EmailOTP.objects.filter(user=user).first()

        key_attempts = f"otp_attempts_{user_id}"
        key_lock = f"otp_locked_{user_id}"
        now = timezone.now().timestamp()

        # Check lock status
        locked_until = cache.get(key_lock)
        if locked_until and float(locked_until) > now:
            return render(request, "accounts/verifyotp.html", {"error": "Too many failed attempts. Try again after 5 minutes."})

        if otp_record and otp_record.otp == otp_entered:
            # Successful, reset counters
            cache.delete(key_attempts)
            cache.delete(key_lock)
            login(request, user)
            if user.profile.s_vendor != True and user.is_staff != True:
                return redirect('home')
            elif user.profile.s_vendor == True and user.is_staff != True:
                return redirect('vendor_dashboard')
            elif user.is_staff == True:
                return redirect('custom_admin_dashboard')
            else:
                messages.error(request, "Invalid user role")
                return redirect('login')
        else:
            attempts = cache.get(key_attempts, 0) + 1
            cache.set(key_attempts, attempts, LOCK_TIME)
            if attempts >= MAX_ATTEMPTS:
                lock_until = now + LOCK_TIME
                cache.set(key_lock, lock_until, LOCK_TIME)
                return render(request, "accounts/verifyotp.html", {"error": "Too many failed attempts. Try again after 5 minutes."})
            else:
                return render(request, "accounts/verifyotp.html", {"error": "Invalid or expired OTP"})

    return render(request, "accounts/verifyotp.html")



# @login_required
# def profile_page(request):
#     categories = Category.objects.all()
#     orders = Order.objects.filter(user=request.user).order_by('-placed_at')  # Fetch user orders
#     Addresss = Address.objects.filter(user=request.user)
#     if hasattr(request.user, 'profile'):
#         profile = request.user.profile
#     else:
#         profile = Profile.objects.create(user=request.user)

#     if request.method == "POST":
#         # Update user's name if "name" is submitted (optional: split into first/last)
#         name = request.POST.get("name", "").strip()
#         if name:
#             if ' ' in name:
#                 request.user.first_name, request.user.last_name = name.split(' ', 1)
#             else:
#                 request.user.first_name = name
#                 request.user.last_name = ""
#         request.user.email = request.POST.get("email", request.user.email)
#         request.user.save()
#         profile.phone_number = request.POST.get("phone_number", profile.phone_number)
#         # Checkbox: checked if present, False if not
#         profile.promotions = 'promotions' in request.POST
#         profile.save()
#         return redirect("profile_page")
#     return render(request, "accounts/profile.html", { "profile": profile, "categories": categories,"orders": orders,"Addresss":Addresss})


@login_required
def profile_page(request):
    categories = Category.objects.order_by('?')[:4]
    categories1 = Category.objects.all()
    orders = Order.objects.filter(user=request.user).order_by("-placed_at")
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()
    categories_list = Category.objects.all()[4:]
    if hasattr(request.user, "profile"):
        profile = request.user.profile
    else:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        # ----- Address Form -----
        if "address_line" in request.POST:  
            address_line = request.POST.get("address_line")
            city = request.POST.get("city")
            is_default = request.POST.get("is_default") == "on"

            address = Address.objects.create(
                user=request.user,
                address_line=address_line,
                city=city,
                is_default=is_default,
            )

            if is_default:
                Address.objects.filter(user=request.user).exclude(pk=address.pk).update(
                    is_default=False
                )

            return redirect("profile_page")

        # ----- Profile Form -----
        else:
            name = request.POST.get("name", "").strip()
            if name:
                if " " in name:
                    request.user.first_name, request.user.last_name = name.split(" ", 1)
                else:
                    request.user.first_name = name
                    request.user.last_name = ""
            request.user.email = request.POST.get("email", request.user.email)
            request.user.save()

            profile.phone_number = request.POST.get("phone_number", profile.phone_number)
            profile.promotions = "promotions" in request.POST
            profile.save()

            return redirect("profile_page")

    addresses = Address.objects.filter(user=request.user,is_default=True)

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "categories": categories,
            "orders": orders,
            "addresses": addresses,  # so you can display saved addresses,
            "categories1":categories1,
            "cartcount":cartcount,
            "categories_list":categories_list
        },
    )


from django.http import JsonResponse

def resend_otp(request):
    user_id = request.session.get("otp_user_id")
    if not user_id:
        messages.error(request, "Session expired. Please enter your email again.")
        return redirect("send_otp")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please try again.")
        return redirect("send_otp")

    # ✅ Generate new OTP
    otp = str(random.randint(100000, 999999))
    EmailOTP.objects.update_or_create(user=user, defaults={"otp": otp})

    send_mail(
        "Your OTP Code (Resent)",
        f"Your new OTP is {otp}. It will expire in 5 minutes.",
        "yourgmail@gmail.com",
        [user.email],
    )

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect("verify_otp")








