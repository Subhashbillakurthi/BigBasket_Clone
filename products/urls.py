from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    # path('search_suggest/', views.product_search_suggest, name='search_suggest'),
    path('wishlist/', views.wishlist_and_cart, name='wishlist_and_cart'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('search/', views.product_search, name='product_search'),
    path("wishlist/move-to-cart/<int:product_id>/", views.move_to_cart, name="move_to_cart"),
    path('category/<str:category_name>/', views.category_products_by_name, name='category_products'),
    path("remove/<int:item_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
]
