from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render 
from . import views
from .views import *

urlpatterns = [
    path('sign_in/', Sign_In.as_view(), name= 'Sign_in'),
    path('sign_up/', Sign_Up.as_view(), name= 'Sign_up'),
    path('forgot_password/', ForgotPassword.as_view(), name= 'Forgot_password'),
    # xác thực OTP và đăng ký trong đăng ký
    path('validate_otp_and_register/', views.validate_otp_and_register, name='validate_otp_and_register'),
    # gửi lại mật khẩu trong đăng ký và quên mật khẩu
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    # xác thực OTP quên mật khẩu
    path('validate_otp_fogotpassword/', views.validate_otp_of_ForgotPassword, name='validate_otp_of_ForgotPassword'),

    path('new_password/', New_password.as_view(), name= 'New_Password'),
    path('trangchu_guest/', views.TrangChu_guest, name= 'TrangChu_guest'),
    path('trangchu_customer/', views.TrangChu_customer, name= 'TrangChu_customer'),
    path('trangOTP/', views.trangOTP, name= 'trangOTP'),
    path('header_guest/', views.header_guest, name='header'),
    path('header_customer/', views.header_customer, name='header1'),
    path('menu/', views.menu, name='menu'),
    path('footer/', views.footer, name='footer'),
    path('History/', views.History, name= 'History'),
    path('fee_guest/', views.fee_guest, name='fee_guest'),
    path('fee_customer/', views.fee_customer, name='fee_customer'),
    path('san_guest/', views.san_guest, name='san_guest'),
    path('san_customer/', views.san_customer, name='san_customer'),
    path('bao_cao/', views.bao_cao, name='bao_cao'),
    path('checkin/', views.checkin, name='checkin'),
    path('dang_ky/', views.dangky, name='dang_ky'),
    path('lichThiDau/', views.lichThiDau, name='lichThiDau'),
    path('them_san/', views.themSan, name='them_san'),
    path('QuanLyThongTinSan/', views.QuanLyThongTinSan, name='QuanLyThongTinSan'),
    path('QuanLyTaiKhoan/', views.QuanLyTaiKhoan, name='QuanLyTaiKhoan'),
  

    path('add_timeslot_template/', views.add_timeslot_template, name='add_timeslot_template'),

]
# coi url


