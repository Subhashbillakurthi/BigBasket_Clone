# products/views.py
from itertools import product
from django.shortcuts import render
from .models import Product  # Your product model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Category,SubSubCategory
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product,Category
from .models import WishlistItem
from cart.models import CartItem
from django.db.models import Sum
from django.contrib.auth.models import AnonymousUser

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/category_listing.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    packs = product.packs.all()
    categories = Category.objects.all()
    categories1 = Category.objects.order_by('?')[:4]
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()
    categories_list = Category.objects.all()[4:]
    return render(request, "products/product_detail.html", {
        "product": product,
        "packs": packs,
        "categories": categories,
        'categories1' : categories1,
        "cartcount":cartcount,
        "categories_list":categories_list
    })

def category_products(request, category_id):
    products = Product.objects.filter(main_category_id=category_id)
    category = Category.objects.get(id=category_id)
    categories = Category.objects.all()[:4]
    categories1 = Category.objects.all()
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()
    categories_list = Category.objects.all()[4:]
    price_filters = request.GET.getlist('price')

    if price_filters:
        q = Q()
        for pf in price_filters:
            if pf == '1to20':
                q |= Q(price__gte=1, price__lte=20)
            elif pf == '21to50':
                q |= Q(price__gte=21, price__lte=50)
            elif pf == '51to100':
                q |= Q(price__gte=51, price__lte=100)
            elif pf == '101to200':
                q |= Q(price__gte=101, price__lte=200)
            elif pf == '201to500':
                q |= Q(price__gte=201, price__lte=500)
        products = products.filter(q)

    brand_selected = request.GET.get('brand')
    if brand_selected:
        brands = brand_selected.split(',')
        products = products.filter(brand__in=brands)

    # Sorting if any (optional)
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    price_selected = request.GET.getlist("price")   # ✅ getlist
    brand_selected = request.GET.getlist("brand")   # ✅ getlist
    sort = request.GET.get("sort")
    context = {
        "price_selected": price_selected,
        "brand_selected": brand_selected,
        "sort": sort,
        "categories_list":categories_list
    }

    discount = request.GET.get('discount')

    if discount == '0to25':
        products = products.filter(discount_percent__gte=0, discount_percent__lte=25)
    elif discount == '25plus':
        products = products.filter(discount_percent__gt=25)

    return render(request, 'products/category_listing.html', {'products': products, **context,'discount_selected': discount,"category": category,"categories": categories,"categories1":categories1,"cartcount":cartcount})

def product_search(request):
    q = request.GET.get('q', '').strip()
    categories = Category.objects.order_by('?')[:4]
    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    return render(request, 'products/category_listing.html', {
        'query': q,
        'products': products,
        'categories': categories
    })




@login_required
@require_POST
def add_to_wishlist(request, product_id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    if int(data.get('product_id', 0)) != product_id:
        return HttpResponseBadRequest('Product ID mismatch')

    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)

    return JsonResponse({'status': 'success', 'message': 'Added to wishlist'})



@login_required
def wishlist_and_cart(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
    categories = Category.objects.all()[:4]
    categories_list = Category.objects.all()[4:]
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()
    return render(request, 'products/wishlist.html', {
        'wishlist_items': wishlist_items,
        'categories':categories,
        "categories_list":categories_list,
        "cartcount":cartcount
    })

@login_required
@require_POST
def move_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Just check normal POST
    if str(request.POST.get("product_id")) != str(product_id):
        return HttpResponseBadRequest("Product ID mismatch")

    # ✅ Add to cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # ✅ Remove from wishlist
    WishlistItem.objects.filter(user=request.user, product=product).delete()

    return redirect("products:wishlist_and_cart")

def category_products_by_name(request, category_name):
    category_name_clean = category_name.strip()
    # Get SubSubCategory instance
    category = get_object_or_404(SubSubCategory, name__iexact=category_name_clean)
    categories = Category.objects.all()[:4]
    categories1 = Category.objects.all()
    # Fetch all products related to this category (sub-sub category)
    products = Product.objects.filter(category=category)
    if isinstance(request.user, AnonymousUser):
        cartcount = 0
    else:
        cartcount = CartItem.objects.filter(user=request.user).count()
    
    print("Category:", category)
    print("Number of products:", products.count())
    
    return render(request, 'products/category_listing.html', {'category': category, 'products': products,"categories":categories,'categories1':categories1,"cartcount":cartcount})

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    return JsonResponse({"status": "success"})