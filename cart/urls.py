from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/add/<int:product_id>/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    
]

