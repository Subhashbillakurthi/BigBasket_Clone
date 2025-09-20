from django.shortcuts import render
from products.models import Product,Category
from cart.models import CartItem
from django.contrib.auth.models import AnonymousUser

def home(request):
    products = Product.objects.order_by('-id')[:6]
    products1 = Product.objects.all()
    categories = Category.objects.all()[:4]
    categories1 = Category.objects.all()
    categories_list = Category.objects.all()[4:]
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()
    maincategories = Category.objects.prefetch_related(
        "subcategories__subsubcategories"
    ).all()
    return render(request, "base.html", {
        "products": products,
        'products1' :products1,
        "categories": categories,   # ✅ add this
        "maincategories":maincategories,
        "categories1":categories1,
        "cartcount":cartcount,
        "categories_list":categories_list
    })


def nav(request): 
    categories = Category.objects.all()[:4]
    categories1 = Category.objects.all()
    cartcount = CartItem.objects.all().count()
    maincategories = Category.objects.prefetch_related(
        "subcategories__subsubcategories"
    ).all()
    print("cartcount",cartcount)
    return render(request, "navbar.html", { 
        "categories": categories,   # ✅ add this
        "maincategories":maincategories,
        "categories1":categories1,
        "cartcount":cartcount
    })


