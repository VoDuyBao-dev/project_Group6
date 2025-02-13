from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render 
from . import views
from .views import *



urlpatterns = [
    path('', views.TrangChu, name= 'TrangChu'),
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
   
    # Tìm kiếm sân:
    path('SearchCourt/', SearchCourt.as_view(), name= 'SearchCourt'),
    path('DangKyTaiKhoanThanhToan/', DangKyTaiKhoanThanhToan.as_view(), name='DangKyTaiKhoanThanhToan'),
    path('header_user/', views.header_user, name='header_user'),
    path('menu/', views.menu, name='menu'),
    path('footer/', views.footer, name='footer'),
    path('History/', views.History, name= 'History'),
    path('price_list/', views.price_list, name='price_list'),
   
   
    path('San/', views.San, name='San'),
    path('bao_cao/', views.bao_cao, name='bao_cao'),
    path('checkin/', views.checkin, name='checkin'),
    
    path('lichThiDau/', views.lichThiDau, name='lichThiDau'),
    path('them_san_moi/', views.them_san_moi, name='them_san_moi'),
    path('them_san/', views.them_san, name='them_san'),
    path('payment/<str:booking_id>/<str:court_id>/', views.payment, name='payment'),
    path('payment/', views.payment, name='payment'),
    path('booking/<str:court_id>/', views.booking_view, name='booking'),

    path('manager_taikhoan/', views.manager_taikhoan, name='manager_taikhoan'),
    path('manager_san/', views.manager_san, name='manager_san'),

    path('menu_manager/', views.menu_manager, name='menu_manager'),
    path('header_guest/', views.header_guest, name='header'),
    path('header_customer/', views.header_customer, name='header1'),
    path('manage_time_slots/', views.manage_time_slots, name='manage_time_slots'),
    path('delete_time_slot/<str:slot_id>/', views.delete_time_slot, name='delete_time_slot'),
    path('ThongTinCaNhan/', views.ThongTinCaNhan, name='ThongTinCaNhan'),
    path('ChinhSuaThongTin', views.ChinhSuaThongTin, name='ChinhSuaThongTin'),

    path('court/edit/<str:court_id>/', edit_court, name='edit_court'),
    path('court/delete/<str:court_id>/', delete_court, name='delete_court'),
] 
# coi url

