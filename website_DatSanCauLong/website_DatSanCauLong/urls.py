import random
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from asgiref.sync import sync_to_async
# Email
def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(username, otp):
    context = {
        'name': username,
        'otp': otp,
        'system_name': 'Sân Cầu Lông Siêu Cấp Vip Pro'  # Thay bằng tên hệ thống của bạn
    }
    html_content = render_to_string('app1/Email_Sign_up.html', context)
    # Tạo email
    email = EmailMessage(
        subject='Xác nhận đăng kí tài khoản',  # Tiêu đề email
        body=html_content,  # Nội dung email (HTML)
        to=[username],  # Gửi đến email người dùng
    )
    email.content_subtype = 'html'  # Đặt email ở định dạng HTML
    email.send()
