from django.urls import path
from . import views


urlpatterns = [

    path('mobile/', views.PhoneVerifyView.as_view(), name='PhoneVerifyView'),
    
    path('otp/', views.OTPVerifyView.as_view(), name='OTPVerifyView'),

    path('recipient_profile/', views.RecipientProfileView.as_view(), name='RecipientProfileView'),

    path('recipient_details/', views.RecipientDetailView.as_view(), name='RecipientDetailView'),

    path('send_thanks/', views.SendThanksView.as_view(), name='SendThanksView'),
]
