from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', Sign_In.as_view(), name= 'Sign_in'),
    path('signup/', Sign_Up.as_view(), name= 'Sign_up'),
   
    path('forgotpassword/', views.Forgot_password, name= 'Forgot_password'),
    path('newpassword/', views.New_password, name= 'New_password'),
    path('trangchu/', views.TrangChu, name= 'TrangChu'),
    path('trangOTP/', views.trangOTP, name= 'trangOTP'),
    path('validate_otp_and_register/', views.validate_otp_and_register, name='validate_otp_and_register'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),


]
