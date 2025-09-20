from django.contrib import admin
from .models import Order, OrderItem,DeliverySlot

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliverySlot)
