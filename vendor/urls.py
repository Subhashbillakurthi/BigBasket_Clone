from django.urls import path
from . import views
 

urlpatterns = [
    path("dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("edit_vendor", views.vendor_details_edit, name="vendor_details_edit"),
 
    # Product CRUD
    path("products/add/", views.add_product, name="vendor_add_product"),
    path("products/edit/<int:pk>/", views.edit_product, name="vendor_edit_product"),
    path("products/delete/<int:pk>/", views.delete_product, name="vendor_delete_product"),

    # Category CRUD
    path("categories/add/", views.vendor_add_category, name="vendor_add_category"),
    path("categories/edit/<int:pk>/", views.vendor_edit_category, name="vendor_edit_category"),
    path("categories/delete/<int:pk>/", views.vendor_delete_category, name="vendor_delete_category"),


    # order staus update 
    path('ststua_order/<int:order_id>/update-status/', views.vendor_update_order_status, name='vendor_update_order_status'),

    path("vendor_list_of_orders/", views.vendor_all_orders, name="vendor_all_orders"),


]