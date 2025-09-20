from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_admin_dashboard, name='custom_admin_dashboard'),

    # Address - View only (no CRUD)
    # Removed add/edit/delete

    # Products CRUD
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

    # Orders - only status update
    path('orders/view/<int:pk>/', views.view_order, name='view_order'),
    path('orders/status/<int:pk>/', views.update_order_status, name='update_order_status'),

    # Categories CRUD
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Users CRUD
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
]
