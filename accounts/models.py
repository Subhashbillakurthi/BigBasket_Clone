from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)


@receiver(post_save, sender=User)
def create_email_otp(sender, instance, created, **kwargs):
    if created:
        EmailOTP.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=32, blank=True)
    s_vendor = models.BooleanField(default=False, blank=True)
    promotions = models.BooleanField(default=True)
    image = models.TextField(default=False, blank=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_email = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=100, blank=True, null=True)
    address_line = models.TextField()
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64, blank=True, null=True)
    pincode = models.CharField(max_length=12, blank=True, null=True)
    address_type = models.CharField(max_length=12, blank=True, null=True,default="home")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.city}"
