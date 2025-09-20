from django.contrib import admin

# Register your models here.
from .models import EmailOTP,Profile,Address
admin.site.register(EmailOTP)
admin.site.register(Profile)
admin.site.register(Address)
