from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from django.contrib.auth.models import User
from products.models import Product,Category
from orders.models import Order, OrderItem, DeliverySlot
from cart.models import CartItem
from .forms import AddressForm, ProductForm, OrderForm,CategoryForm, UserForm 
from django import forms


@login_required
def custom_admin_dashboard(request):
    context = {
        "users": User.objects.all(),
        "addresses": Address.objects.all(),
        "products": Product.objects.all(),
        "orders": Order.objects.all(),
        "order_items": OrderItem.objects.all(),
        "delivery_slots": DeliverySlot.objects.all(),
        "cart_items": CartItem.objects.all(),
        "categories": Category.objects.all(),
    }
    return render(request, "dashboard/dashboard.html", context)


# ------------------------
# Address CRUD
# ------------------------
@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = AddressForm()
    return render(request, "dashboard/form.html", {"form": form, "title": "Add Address"})


@login_required
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = AddressForm(instance=address)
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Address"})


@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    return redirect("custom_admin_dashboard")


# ------------------------
# Product CRUD
# ------------------------
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = ProductForm()
    return render(request, "dashboard/form.html", {"form": form, "title": "Add Product"})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = ProductForm(instance=product)
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Product"})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("custom_admin_dashboard")


# ------------------------
# Order CRUD
# ------------------------
@login_required
def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = OrderForm()
    return render(request, "dashboard/form.html", {"form": form, "title": "Add Order"})


@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = OrderForm(instance=order)
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Order"})


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect("custom_admin_dashboard")


# ------------------------
# Category CRUD
# ------------------------
@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = CategoryForm()
    return render(request, "dashboard/form.html", {"form": form, "title": "Add Category"})


@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = CategoryForm(instance=category)
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Category"})


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("custom_admin_dashboard")


# ------------------------
# User CRUD
# ------------------------
@login_required
def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = UserForm()
    return render(request, "dashboard/form.html", {"form": form, "title": "Add User"})


@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = UserForm(instance=user)
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit User"})


@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect("custom_admin_dashboard")

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status'] 

@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("custom_admin_dashboard")
    else:
        form = OrderStatusForm(instance=order)
    return render(request, "dashboard/form.html", {"form": form, "title": f"Update Status for Order #{order.id}"})


@login_required
def view_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, "dashboard/view_order.html", {
        "order": order,
        "order_items": order_items,
    })
