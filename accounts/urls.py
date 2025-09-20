from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('otp/', views.send_otp, name='send_otp'),
    path('verifyotp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
]
