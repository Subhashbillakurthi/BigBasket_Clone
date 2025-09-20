# payments/views.py
import json
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Order
 
# stripe.api_key = settings.STRIPE_SECRET_KEY

# @csrf_exempt
# def create_checkout_session(request):
#     # Expect JSON: {"amount": 49900, "currency":"inr", "name":"Wireless Headphones", "reference":"ORD123"}
#     if request.method != "POST":
#         return JsonResponse({"error": "POST required"}, status=405)
#     try:
#         payload = json.loads(request.body.decode())
#         amount = int(payload["amount"])
#         currency = payload.get("currency", "inr")
#         name = payload.get("name", "Order")
#         reference = payload.get("reference", f"ORD-{timezone.now().timestamp()}")

#         order, _ = Order.objects.get_or_create(
#             reference=reference,
#             defaults={"amount": amount, "currency": currency}
#         )

#         session = stripe.checkout.Session.create(
#             mode="payment",
#             payment_method_types=["card"],
#             line_items=[{
#                 "price_data": {
#                     "currency": currency,
#                     "product_data": {"name": name},
#                     "unit_amount": amount,
#                 },
#                 "quantity": 1,
#             }],
#             success_url=f"{settings.PAYMENT_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}&ref={order.reference}",
#             cancel_url=settings.PAYMENT_CANCEL_URL,
#             metadata={"order_reference": order.reference},
#         )
#         order.stripe_checkout_session = session.id
#         order.save(update_fields=["stripe_checkout_session"])
#         return JsonResponse({"checkout_url": session.url})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)

# def success(request):
#     return render(request, "payments/success.html")
# def cancel(request):
#     return render(request, "payments/cancel.html")

# @csrf_exempt
# def stripe_webhook(request):
#     # Verify signature and handle events
#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except ValueError:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError:
#         return HttpResponse(status=400)

#     # Handle Checkout completion -> PaymentIntent events under the hood
#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         order_ref = session.get("metadata", {}).get("order_reference")
#         if order_ref:
#             try:
#                 order = Order.objects.get(reference=order_ref)
#                 order.status = "paid"
#                 order.paid_at = timezone.now()
#                 order.stripe_payment_intent = session.get("payment_intent")
#                 order.save(update_fields=["status", "paid_at", "stripe_payment_intent"])
#             except Order.DoesNotExist:
#                 pass
#     elif event["type"] == "payment_intent.succeeded":
#         pi = event["data"]["object"]
#         # Optional reinforcement: find order by PI and mark paid
#     elif event["type"] == "payment_intent.payment_failed":
#         pi = event["data"]["object"]
#         # Optional: mark order failed
#     return HttpResponse(status=200)

# # payments/views.py (add)
# @csrf_exempt
# def create_payment_intent(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST required"}, status=405)
#     try:
#         payload = json.loads(request.body.decode())
#         amount = int(payload["amount"])
#         currency = payload.get("currency", "inr")
#         reference = payload.get("reference", f"ORD-{timezone.now().timestamp()}")

#         order, _ = Order.objects.get_or_create(
#             reference=reference,
#             defaults={"amount": amount, "currency": currency}
#         )

#         intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency=currency,
#             metadata={"order_reference": order.reference},
#             automatic_payment_methods={"enabled": True},
#         )
#         order.stripe_payment_intent = intent.id
#         order.save(update_fields=["stripe_payment_intent"])
#         return JsonResponse({"clientSecret": intent.client_secret,
#                              "publishableKey": settings.STRIPE_PUBLISHABLE_KEY})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)

