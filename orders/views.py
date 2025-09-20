from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, DeliverySlot
from cart.models import CartItem  # adjust if your cart app is named differently
from datetime import datetime, timedelta
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import  Order, OrderItem
from accounts.models import Address
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import razorpay

# @login_required
# def checkout_view(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     addresses = Address.objects.filter(user=request.user)
    
#     if not cart_items.exists():
#         return redirect('cart:cart')
    
#     # Generate delivery slots
#     slots = []
#     today = datetime.today().date()
#     for i in range(2):
#         date = today + timedelta(days=i)
#         for label in ['7:00 AM - 10:00 AM', '10:00 AM - 1:00 PM']:
#             slots.append({
#                 'date': date.strftime('%Y-%m-%d'),
#                 'slot_label': label,
#                 'display': f"{date.strftime('%a, %d %b')}, Between {label}"
#             })

#     total = sum(item.product.price * item.quantity for item in cart_items)
#     total_mrp = sum((item.product.mrp or item.product.price) * item.quantity for item in cart_items)
#     savings = total_mrp - total if total_mrp > total else 0

#     if request.method == "POST":
#         # ✅ Get delivery slot
#         delivery_data = request.POST.get('delivery_slot')  # e.g. "2025-09-10|7:00 AM - 10:00 AM"
#         slot_date_str, slot_time = delivery_data.split("|")

#         slot_date = datetime.strptime(slot_date_str.strip(), "%Y-%m-%d").date()
#         slot_obj, _ = DeliverySlot.objects.get_or_create(
#             date=slot_date,
#             slot_label=slot_time.strip()
#         )

#         # ✅ Create Razorpay order
#         amount_paise = int(float(total) * 100)
#         client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
#         payment = client.order.create({'amount': amount_paise, 'currency': 'INR', 'payment_capture': 1})

#         # ✅ Create Django order with slot + Razorpay id
#         order = Order.objects.create(
#             user=request.user,
#             address="User Primary Address",  # replace with real address
#             delivery_slot=slot_obj,
#             total_amount=total,
#             savings=savings,
#             status="Placed ✅",
#             razor_pay_id=payment['id']
#         )

#         # Save items
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product.name,
#                 quantity=item.quantity,
#                 price=item.product.price,
#                 mrp=item.product.mrp or item.product.price,
#                 image_url=getattr(item.product, 'image', '')
#             )
#         cart_items.delete()

#         return render(request, 'payments/payment.html', {
#             "payment": payment,
#             "order": order,
#             "cart_items": cart_items,
#             "slots": slots,
#             "total": total,
#             "savings": savings,
#             "addresses": addresses,
#         })

#     return render(request, 'orders/checkout.html', {
#         "cart_items": cart_items,
#         "slots": slots,
#         "total": total,
#         "savings": savings,
#         "addresses": addresses,
#     })




# @login_required
# def order_success_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     return render(request, 'orders/order_success.html', {"order": order})

# @login_required
# def orders_list_view(request):
#     orders = Order.objects.filter(user=request.user).order_by('-placed_at')
#     return render(request, 'orders/orders_list.html', {'orders': orders})
