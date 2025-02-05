from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render 
from . import views
from .views import *

urlpatterns = [
    path('sign_in/', Sign_In.as_view(), name= 'Sign_in'),
    path('Logout/', views.Logout, name='Logout'),
    path('sign_up/', Sign_Up.as_view(), name= 'Sign_up'),
    path('forgot_password/', ForgotPassword.as_view(), name= 'Forgot_password'),
    path('trangOTP/', views.trangOTP, name= 'trangOTP'),
    # xác thực OTP và đăng ký trong đăng ký
    path('validate_otp_and_register/', views.validate_otp_and_register, name='validate_otp_and_register'),
    # gửi lại mật khẩu trong đăng ký và quên mật khẩu
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    # xác thực OTP quên mật khẩu
    path('validate_otp_fogotpassword/', views.validate_otp_of_ForgotPassword, name='validate_otp_of_ForgotPassword'),
    path('new_password/', New_password.as_view(), name= 'New_Password'),
    path('TrangChu/', views.TrangChu, name= 'TrangChu'),
   
    # Tìm kiếm sân:
    path('SearchCourt/', SearchCourt.as_view(), name= 'SearchCourt'),
    
    
    path('header_user/', views.header_user, name='header_user'),
    path('menu/', views.menu, name='menu'),
    path('footer/', views.footer, name='footer'),
    path('History/', views.History, name= 'History'),
    path('price_list/', views.price_list, name='price_list'),
   
    path('San/', views.San, name='San'),
    path('bao_cao/', views.bao_cao, name='bao_cao'),
    path('checkin/', views.checkin, name='checkin'),
    path('dang_ky/', views.dangky, name='dang_ky'),
    path('lichThiDau/', views.lichThiDau, name='lichThiDau'),
    path('them_san/', views.themSan, name='them_san'),
    path('payment/', views.Payment, name='payment'),
    path('booking/', views.Booking, name='booking'),
    # path('manager_taikhoan/', views.manager_taikhoan, name='manager_taikhoan'),
    # path('manager_san/', views.manager_san, name='manager_san'),

    path('fee_customer/', views.fee_customer, name='fee_customer'),
    path('manage_time_slots/', views.manage_time_slots, name='manage_time_slots'),
    path('delete_time_slot/<str:slot_id>/', views.delete_time_slot, name='delete_time_slot'),
]
# coi url


