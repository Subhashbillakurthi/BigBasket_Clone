# vendor/models.py
from django.db import models
from accounts.models import Profile

class Vendor(models.Model): 
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'s_vendor': True},
        null=True,
        blank=True,
    )

    shop_name = models.CharField(max_length=150)

    # Business / tax
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)

    # Contact
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    shop_image = models.TextField(default="",blank=True, null=True) 

    def __str__(self):
        return self.shop_name 