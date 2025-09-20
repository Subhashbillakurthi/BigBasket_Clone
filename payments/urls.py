# payments/urls.py
from django.urls import path
from . import views

# urlpatterns = [
#     path("checkout/", views.create_checkout_session, name="create_checkout_session"),       # POST
#     path("element/intent/", views.create_payment_intent, name="create_payment_intent"),     # POST (Payment Element)
#     path("success/", views.success, name="payment_success"),                                # GET
#     path("cancel/", views.cancel, name="payment_cancel"),                                   # GET
#     path("webhook/", views.stripe_webhook, name="stripe_webhook"),                          # POST
# ]
