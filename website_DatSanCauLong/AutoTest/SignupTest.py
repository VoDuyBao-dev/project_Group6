import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Get_OTP_Email import get_otp_from_gmail

class TestUserSignUp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # Mở Chrome full màn hình
        self.driver.implicitly_wait(10)  # Chờ tối đa 10s nếu phần tử chưa xuất hiện

    def tearDown(self):
        self.driver.quit()  # Đóng trình duyệt sau khi test xong
    

    def test_user_SignUp(self):
        print("Bắt đầu kiểm thử đăng ký sân cầu lông")
        driver = self.driver
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)  
        
        # Tìm nút "Đăng ký"
        SignUp_button = driver.find_element(By.CSS_SELECTOR, ".btn.signup-btn")  # Hoặc By.CLASS_NAME nếu có class
        time.sleep(2)
        # Nhấn vào nút "Đăng kí"
        SignUp_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi chuyển trang

        # Kiểm tra kết quả
        self.assertIn("Đăng kí", driver.title)  # Kiểm tra xem tiêu đề có đúng là trang Đăng kí không
        # In kết quả ra terminal
        print("Đã nhấn vào nút Đăng kí và chuyển hướng thành công.")
        # Tìm phần tử
        eye_password_button = driver.find_element(By.ID, "password-icon")
        eye_confirm_password_button = driver.find_element(By.ID, "confirm-password-icon")
        inputUserName = driver.find_element(By.ID, "username_SignUp")
        inputFullName = driver.find_element(By.ID, "full_name")
        inputPassword = driver.find_element(By.ID, "id_password")
        inputConfirmPassword = driver.find_element(By.ID, "id_confirm_password")

        # Nhập thiếu trường
        inputUserName.send_keys("voduybao19052005@gmail.com")
        inputUserName.send_keys(Keys.RETURN)
        time.sleep(2)

        # Nhập sai định dạng tên tài khoản và confirm password
        inputUserName.clear()
        time.sleep(2)
        inputUserName.send_keys("voduybao1905200gmail")
        time.sleep(1)  # Nghỉ 1s trước khi nhập mật khẩu
        inputFullName.send_keys("Võ Duy Bảo")
        print("Tới nhập full name")
        inputPassword.send_keys("12345")
        print("Tới nhập password")
        inputConfirmPassword.send_keys("1234567")
        eye_password_button.click()
        eye_confirm_password_button.click()
        time.sleep(1.5)  # Chờ 1.5s trước khi nhấn Enter
        inputConfirmPassword.send_keys(Keys.RETURN)
        time.sleep(3)  # Chờ 3s để trang load lại
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("test sai định dạng tài khoản và xác nhận lại mật khẩu thành công")
        except:
            print("Không tìm thấy thông báo lỗi")

        # Nhập lại đúng định dạng và confirm password
        inputUserName = driver.find_element(By.ID, "username_SignUp")
        inputPassword = driver.find_element(By.ID, "id_password")
        inputConfirmPassword = driver.find_element(By.ID, "id_confirm_password")
        eye_password_button = driver.find_element(By.ID, "password-icon")
        eye_confirm_password_button = driver.find_element(By.ID, "confirm-password-icon")
        inputUserName.clear()
        inputUserName.send_keys("voduybao192005@gmail.com")
        time.sleep(1)
        inputPassword.send_keys("1234")
        inputConfirmPassword.send_keys("1234")
        eye_password_button.click()
        eye_confirm_password_button.click()
        print("Nhấn xem mật khẩu")
        time.sleep(1.5)
        inputConfirmPassword.send_keys(Keys.RETURN)
        # Kiểm tra xem đăng ký có đúng thông tin không và chuyển đến trang nhập OTP
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Trang OTP"))
            actualTitle = driver.title
            print("Tiêu đề sau khi nhấn nút đăng ký:", actualTitle)
            self.assertEqual(actualTitle, "Trang OTP")
            print("Test nhập thông tin đăng kí thành công và chuyển đến trang nhập OTP")
        except:
            print("Test nhập thông tin đăng kí thất bại")

        time.sleep(1)
        # Lấy mã OTP
        # Thông tin tài khoản Gmail
        email_user = "voduybao192005@gmail.com"
        email_password = "sgnk ryus bmeb zcxt"

        # Lấy mã OTP
        otp_code = get_otp_from_gmail(email_user, email_password)

        if otp_code:
          print("Mã OTP là:", otp_code)
        else:
          print("Không thể lấy mã OTP.")

        # Tìm phần tử để nhập otp
        inputOTP = driver.find_elements(By.CLASS_NAME, "otp-input")
        print("chọn ô nhập OTP thành công")

       
        # Kiểm tra số lượng ô nhập
        # Điền sai mã OTP
        # Điền từng chữ số của OTP vào các ô nhập
        for i in range (len(inputOTP)):
            inputOTP[i].send_keys(1)
        print("Đã điền mã OTP thành công.")

        time.sleep(2)
        # tìm nút gửi mã OTP
        submit_OTP = driver.find_element(By.ID, "submit-otp")
        submit_OTP.click()
        time.sleep(3)
        # Xử lý thông báo JS nếu xuất hiện
        try:
            alert = driver.switch_to.alert
            alert_message = alert.text
            print("Thông báo từ JS:", alert_message)
            time.sleep(1)
            alert.accept()
        except NoAlertPresentException:
            print("Không có thông báo JS nào xuất hiện.")

        time.sleep(2)
        # gửi lại mã OTP
        submit_resend_OTP = driver.find_element(By.ID, "resend-otp")
        submit_resend_OTP.click()
        time.sleep(10)

        # Lấy mã OTP
        otp_code = get_otp_from_gmail(email_user, email_password)

        if otp_code:
          print("Mã OTP là:", otp_code)
        else:
          print("Không thể lấy mã OTP.")
        
        # Xử lý thông báo JS nếu xuất hiện
        try:
            alert = driver.switch_to.alert
            alert_message = alert.text
            print("Thông báo từ JS:", alert_message)
            time.sleep(1)
            alert.accept()
        except NoAlertPresentException:
            print("Không có thông báo JS nào xuất hiện.")

        # Điền từng chữ số của OTP vào các ô nhập
        for i, digit in enumerate(otp_code):
            inputOTP[i].clear()
            inputOTP[i].send_keys(digit)
        print("Đã điền mã OTP thành công.")
        time.sleep(2)

        # gửi mã OTP
        submit_OTP.click()
        time.sleep(3)
        try:
            alert = driver.switch_to.alert
            alert_message = alert.text
            print("Thông báo từ JS:", alert_message)
            time.sleep(2)
            alert.accept()
        except NoAlertPresentException:
            print("Không có thông báo JS nào xuất hiện.")
        
        # Kiểm tra xem đã chuyển hướng đến trang đăng nhập chưa
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Đăng nhập"))
            actualTitle = driver.title
            self.assertEqual(actualTitle, "Đăng nhập")
            print("Test đăng ký thành công")
        except:
            print("Test đăng ký thất bại")

        time.sleep(3)

if __name__ == "__main__":
    unittest.main()
