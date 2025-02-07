from django.contrib import admin
from django.urls import path, include
from . import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('app1.urls')),  # ✅ Kiểm tra 'app1/urls.py' có tồn tại không

    path('sign_in/', views.Sign_In.as_view(), name='Sign_in'),
    path('sign_up/', views.Sign_Up.as_view(), name='Sign_up'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='Forgot_password'),

    # Xác thực OTP và đăng ký
    path('validate_otp_and_register/', views.validate_otp_and_register, name='validate_otp_and_register'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('validate_otp_fogotpassword/', views.validate_otp_of_ForgotPassword, name='validate_otp_of_ForgotPassword'),

    path('new_password/', views.New_password.as_view(), name='New_Password'),
    path('trangchu_guest/', views.TrangChu_guest, name='TrangChu_guest'),
    path('trangchu_customer/', views.TrangChu_customer, name='TrangChu_customer'),
    path('trangOTP/', views.trangOTP, name='trangOTP'),
    path('header_guest/', views.header_guest, name='header_guest'),
    path('header_customer/', views.header_customer, name='header_customer'),
    path('menu/', views.menu, name='menu'),
    path('footer/', views.footer, name='footer'),
    path('History/', views.History, name='History'),
    path('fee_guest/', views.fee_guest, name='fee_guest'),
    path('fee_customer/', views.fee_customer, name='fee_customer'),
    path('san_guest/', views.san_guest, name='san_guest'),
    path('san_customer/', views.san_customer, name='san_customer'),
    path('bao_cao/', views.bao_cao, name='bao_cao'),
    path('checkin/', views.checkin, name='checkin'),
    path('dang_ky/', views.dangky, name='dang_ky'),
    path('lichThiDau/', views.lichThiDau, name='lichThiDau'),
    path('them_san/', views.themSan, name='them_san'),
    path('payment/', views.payment, name='payment'),
    path('booking/', views.booking, name='booking'),
    path('manager_taikhoan/', views.manager_taikhoan, name='manager_taikhoan'),
    path('manager_san/', views.manager_san, name='manager_san'),
]
