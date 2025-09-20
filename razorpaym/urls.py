from django.urls import path
from . import views

app_name = "razorpaym"
urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
     path("razorpaym_add_address/", views.razorpaym_add_address, name="razorpaym_add_address"),
]
