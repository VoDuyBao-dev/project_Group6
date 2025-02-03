from django.contrib import admin
from django.urls import path, include
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
    path('trangchu/', views.TrangChu, name= 'TrangChu'),
    path('trangOTP/', views.trangOTP, name= 'trangOTP'),
# thêm thông tin về giá và thời gian của các lịch đặt sân.
    path('add_timeslot_template/', add_timeslot_template, name='add_timeslot_template'),


]

# coi urls