import imaplib
import email
import re

def get_otp_from_gmail(email_user, email_password):
    try:
        # Kết nối đến máy chủ IMAP của Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_password)

        # Chọn hộp thư đến (INBOX)
        mail.select("inbox")

        # Tìm email mới nhất từ hệ thống gửi OTP (lọc email theo tiêu đề hoặc người gửi)
        status, data = mail.search(None, '(FROM "mariathanhsuong1206@gmail.com")')
        if status != "OK":
            print("Không tìm thấy email nào.")
            return None

        # Lấy ID của email mới nhất
        email_ids = data[0].split()
        latest_email_id = email_ids[-1]

        # Lấy nội dung email
        status, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]

        # Phân tích nội dung email
        email_message = email.message_from_bytes(raw_email)

        # Duyệt qua các phần của email để lấy nội dung
        for part in email_message.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
                charset = part.get_content_charset() or "utf-8"
                body = part.get_payload(decode=True).decode(charset, errors="replace")

                # Tìm mã OTP trong nội dung email
                otp = re.search(r"\b\d{4}\b", body)  # Giả định mã OTP là 4 chữ số
                if otp:
                    return otp.group(0)

        print("Không tìm thấy mã OTP.")
        return None

    except Exception as e:
        print("Lỗi khi truy cập Gmail:", e)
        return None


# Thông tin tài khoản Gmail
# email_user = "voduybao192005@gmail.com"
# email_password = "sgnk ryus bmeb zcxt"

# # Lấy mã OTP
# otp_code = get_otp_from_gmail(email_user, email_password)

# if otp_code:
#     print("Mã OTP là:", otp_code)
# else:
#     print("Không thể lấy mã OTP.")
