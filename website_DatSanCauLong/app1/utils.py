import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Email
def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(username, otp):
    context = {
        'name': username,
        'otp': otp,
        'system_name': 'Sân Cầu Lông Siêu Cấp Vip Pro'  # Thay bằng tên hệ thống của bạn
    }
    html_content = render_to_string('QuanLiUser/email_dangky.html', context)
    # Tạo email
    email = EmailMessage(
        subject='Xác nhận đăng kí tài khoản',  # Tiêu đề email
        body=html_content,  # Nội dung email (HTML)
        from_email='sancaulong@gmail.com',
        to=[username],  # Gửi đến email người dùng
    )
    email.content_subtype = 'html'  # Đặt email ở định dạng HTML
    email.send()

