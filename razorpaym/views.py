import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from accounts.models import *
from products.models import*
from cart.models import *
from orders.models import*
import razorpay 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
@csrf_exempt
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price for item in cart_items)
    savings = sum(item.saved for item in cart_items)
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()

    addresses = request.user.addresses.all()
    slots = DeliverySlot.objects.all()

    razorpay_order = None
    order = None

    if request.method == "POST":
        address_id = request.POST.get("address")
        slot_id = request.POST.get("slot")

        address = get_object_or_404(Address, id=address_id, user=request.user)
        slot = get_object_or_404(DeliverySlot, id=slot_id)

        # ✅ Create Order in DB
        order = Order.objects.create(
            user=request.user,
            address=address,
            delivery_slot=slot,
            total_amount=total_amount,
            savings=savings,
            status="Placed", 
        )

        # Add items to order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                mrp=item.product.mrp,
                image_url=item.product.image if item.product.image else "",
            )

        # ✅ Create Razorpay Order
        razorpay_order = client.order.create({
            "amount": int(total_amount * 100),  # in paise
            "currency": "INR",
            "payment_capture": "1"
        })

        order.razor_pay_id = razorpay_order["id"]
        order.save()

    return render(request, "razorpaym/checkout.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "savings": savings,
        "addresses": addresses,
        "slots": slots,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "razorpay_order": razorpay_order,
        "order": order,
        "cartcount":cartcount,
    })


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        # ✅ Verify signature
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except:
            return redirect("razorpaym:payment_failed")

        # ✅ Mark order as Paid
        order = Order.objects.get(razor_pay_id=razorpay_order_id)
        order.payment_status = "Paid"
        order.save()

        # ✅ Decrease product stock
        for item in order.items.all():
            product = item.product
            if product.quantity and product.quantity >= item.quantity:
                product.quantity -= item.quantity
            else:
                product.quantity = 0
            product.save()

        # ✅ Clear cart
        CartItem.objects.filter(user=request.user).delete()

        return render(request, "razorpaym/success.html", {
            "order": order,
            "razorpay_order_id": razorpay_order_id
        })

    return redirect("razorpaym:checkout")



@csrf_exempt
def payment_failed(request):
    return render(request, "razorpaym/failure.html")




@login_required
def razorpaym_add_address(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        customer_email = request.POST.get("customer_email", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        address_line = request.POST.get("address_line", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        address_type = request.POST.get("address_type", "home")
        is_default = bool(request.POST.get("is_default"))

        # If this address is set as default, unset others
        if is_default:
            Address.objects.filter(user=request.user).update(is_default=False)

        # Save the new address
        Address.objects.create(
            user=request.user,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            address_type=address_type,
            is_default=is_default
        )

        return redirect("razorpaym:checkout")  # or your checkout page route name

    return render(request, "razorpaym/add_address.html")