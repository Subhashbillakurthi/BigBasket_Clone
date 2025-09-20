# payments/models.py
from django.db import models

class Order(models.Model):
    reference = models.CharField(max_length=64, unique=True)
    amount = models.PositiveIntegerField(help_text="Amount in smallest currency unit, e.g., paise")
    currency = models.CharField(max_length=10, default="inr")
    status = models.CharField(max_length=20, default="created")  # created, paid, failed, canceled
    stripe_payment_intent = models.CharField(max_length=128, blank=True, null=True)
    stripe_checkout_session = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.reference} ({self.status})"
