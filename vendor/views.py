from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from accounts.models import Profile
from orders.models import Order
from .forms import ProductForm, CategoryForm , VendorForm
from vendor.models import Vendor
from django.contrib import messages



def get_vendor(request):
    try:
        return Vendor.objects.get(user=request.user.profile)
    except Vendor.DoesNotExist:
        return None
    
@login_required
def vendor_dashboard(request):
    vendor = get_vendor(request)
    if not vendor:
        return redirect("/")

    products = Product.objects.filter(vendor=vendor)
    categories = Category.objects.filter(subcategories__subsubcategories__products__vendor=vendor).distinct()


    recent_orders = (
        Order.objects
        .filter(items__product__vendor=vendor, payment_status="Paid")
        .distinct()
        .order_by('-id')[:6]
    )

    return render(request, "vendor/dashboard.html", {
        "vendor": vendor,
        "products": products,
        "categories": categories,
        "recent_orders": recent_orders,
        "status_choices": Order.STATUS_CHOICES,  # ✅ pass choices
    })




# ---------------- Product CRUD ----------------
@login_required
def add_product(request):
    vendor = get_vendor(request)
    if not vendor:
        return redirect("/")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor  # assign logged-in vendor automatically
            product.save()
            return redirect("vendor_dashboard")
    else:
        form = ProductForm()

    return render(request, "vendor/product_form.html", {"form": form})


@login_required
def edit_product(request, pk):
    vendor = get_vendor(request)
    product = get_object_or_404(Product, pk=pk, vendor=vendor)  # vendor can only edit their own
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = ProductForm(instance=product)

    return render(request, "vendor/product_form.html", {"form": form})

@login_required
def delete_product(request, pk):
    vendor = get_vendor(request)
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    product.delete()
    return redirect("vendor_dashboard")

# ---------------- Category CRUD ----------------

@login_required
def vendor_add_category(request):
    vendor = get_vendor(request)
    if not vendor:
        return redirect("/")

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["name"].strip()

            # Check if category already exists (case-insensitive)
            if Category.objects.filter(name__iexact=category_name).exists():
                # Category already exists, just redirect
                return redirect("vendor_dashboard")

            # Save new category
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = CategoryForm()

    return render(request, "vendor/category_form.html", {"form": form})

 
@login_required
def vendor_edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = CategoryForm(instance=category)

    return render(request, "vendor/category_form.html", {"form": form})

@login_required
def vendor_delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("vendor_dashboard")


@login_required
def vendor_details_edit(request):
    vendor = get_vendor(request)
    if not vendor:
        return redirect("/")

    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = VendorForm(instance=vendor) 
    return render(request, "vendor/vendor_details_edit.html", {"form": form})




#order status update


@login_required
def vendor_update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)

        # Ensure the order includes this vendor’s products
        vendor = get_vendor(request)
        if not order.items.filter(product__vendor=vendor).exists():
            return redirect("vendor_dashboard")  # deny update if vendor not related

        new_status = request.POST.get("status")
        if new_status in ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]:
            order.status = new_status
            order.save()

    return redirect("vendor_dashboard")
  


@login_required
def vendor_all_orders(request):
    vendor = get_vendor(request)
    if not vendor:
        return redirect("/")

    # 🔹 Handle status update form submit
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("new_status")

        if order_id and new_status:
            try:
                order = (
                    Order.objects
                    .filter(pk=order_id, items__product__vendor=vendor, payment_status="Paid")  # ✅ only paid
                    .distinct()
                    .first()
                )
                if order:
                    order.status = new_status
                    order.save(update_fields=["status"])
                    messages.success(request, f"✅ Order #{order.id} updated to {new_status}")
                else:
                    messages.error(request, "❌ Order not found or not assigned to you")
            except Exception as e:
                messages.error(request, f"⚠️ Error updating status: {e}")

        return redirect("vendor_all_orders")

    # 🔹 Get only PAID vendor orders
    orders = (
        Order.objects
        .filter(items__product__vendor=vendor, payment_status="Paid")  # ✅ filter added
        .prefetch_related("items__product", "address", "user")
        .distinct()
        .order_by("-placed_at")
    )

    return render(
        request,
        "vendor/all_orders.html",
        {
            "orders": orders,
            "vendor": vendor,
            "status_choices": Order.STATUS_CHOICES,
        },
    )