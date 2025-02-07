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

class TestUserForgotPassword(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # Mở Chrome full màn hình
        self.driver.implicitly_wait(10)  # Chờ tối đa 10s nếu phần tử chưa xuất hiện

    def tearDown(self):
        self.driver.quit()  # Đóng trình duyệt sau khi test xong
    
    def enter_credentials(self, password):
        # Nhập mật khẩu vào form đăng nhập
        password_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "id_password"))
        )
        
        time.sleep(1)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    def check_error_message(self, message_class, number_mistakes):
        # Kiểm tra sự xuất hiện của thông báo lỗi
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, message_class))
            )
            print(f"test đăng nhập sai lần {number_mistakes}")
        except:
            print(f"Không tìm thấy thông báo lỗi")

    def test_user_SignIn(self):
        print("Bắt đầu kiểm thử quên mật khẩu sân cầu lông")
        driver = self.driver
        driver.get("http://127.0.0.1:8000")
        time.sleep(2)  

        # Tìm nút "Đăng nhập"
        SignIn_button = driver.find_element(By.CSS_SELECTOR, ".btn.login-btn")  

        # Nhấn vào nút "Đăng nhập"
        SignIn_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi chuyển trang

        # Kiểm tra kết quả
        self.assertIn("Đăng nhập", driver.title)  # Kiểm tra xem tiêu đề có đúng là trang đăng nhập không
        # In kết quả ra terminal
        print("Đã nhấn vào nút Đăng nhập và chuyển hướng thành công.")
       
        # Nhập sai định dạng tên tài khoản
        inputUserName = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "id_password")
        
        inputUserName.send_keys("voduybao192005@gmail.com")
        time.sleep(1)  # Nghỉ 1s trước khi nhập mật khẩu
        for i in range(5):
            # Tìm nút xem mật khẩu
            eye_button = driver.find_element(By.ID, "new-password-icon")
            eye_button.click()
            self.enter_credentials("123444")
            self.check_error_message(".alert.alert-danger", i+1)
            time.sleep(2)  # Chờ 2s để trang load lại
        
        time.sleep(3)

        #  Tìm nút quên mật khẩu
        forgot_password_button = driver.find_element(By.ID, "Forgot-Password")
        forgot_password_button.click()

        # Kiểm tra đã đến trang quên mật khẩu chưa
        try:
            self.assertIn("Quên mật khẩu", driver.title)  # Kiểm tra xem tiêu đề có đúng là trang đăng nhập không
            # In kết quả ra terminal
            print("Đã nhấn vào nút quên mật khẩu và chuyển hướng thành công.")
        except:
            print("vào trang quên mật khẩu thất bại")

        time.sleep(2)

        # tìm nút nhập email
        input_username = driver.find_element(By.ID, "id_username_ForgotPassword")  

        # Nhập dữ liệu vào form
        # Nhập lần 1 sai định dạng email
        input_username.send_keys("voduybao192005")
        input_username.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("Test nhập sai định dạng tài khoản thành công")
        except:
            print("Không tìm thấy thông báo lỗi")
        
        time.sleep(3)

        # Test nhập email chưa đăng kí
        input_username = driver.find_element(By.ID, "id_username_ForgotPassword")
        input_username.clear()
        input_username.send_keys("voduybao123@gmail.com")
        input_username.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("Test nhập email chưa đăng kí thành công")
        except:
            print("Không tìm thấy thông báo lỗi")

        time.sleep(3)
        
        # Nhập đúng email đã đăng kí
        # Test nhập email chưa đăng kí
        input_username = driver.find_element(By.ID, "id_username_ForgotPassword")
        input_username.clear()
        time.sleep(1)
        input_username.send_keys("voduybao192005@gmail.com")
        input_username.send_keys(Keys.RETURN)
        # Kiểm tra xem đã chuyển hướng đến Đăng nhập chưa
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Đăng nhập"))
            actualTitle = driver.title
            self.assertEqual(actualTitle, "Đăng nhập")
            print("Test nhập email để lấy lại mật khẩu thành công")
        except:
            print("Test nhập email để lấy lại mật khẩu thất bại")

        time.sleep(2)

        # Lấy mã OTP từ email
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

        # Điền từng chữ số của OTP vào các ô nhập
        for i, digit in enumerate(otp_code):
            inputOTP[i].clear()
            inputOTP[i].send_keys(digit)
        print("Đã điền mã OTP thành công.")
        time.sleep(2)
        # tìm nút gửi mã OTP
        submit_OTP = driver.find_element(By.ID, "submit-otp")
        # gửi mã OTP
        submit_OTP.click()
        time.sleep(5)
        try:
            alert = driver.switch_to.alert
            alert_message = alert.text
            print("Thông báo từ JS:", alert_message)
            time.sleep(2)
            alert.accept()
        except NoAlertPresentException:
            print("Không có thông báo JS nào xuất hiện.")

        time.sleep(3)
        # Chờ cho thẻ input có id: id_new_password xuất hiện 
        try:
            
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "id_new_password")))
            print("Test nhập OTP để lấy lại mật khẩu thành công")
        except:
            print("Test nhập OTP để lấy lại mật khẩu thất bại")

        time.sleep(2)
        
        input_NewPassword = driver.find_element(By.ID, "id_new_password")
        input_Confirm_NewPassword = driver.find_element(By.ID, "id_confirm_new_password")
        # xem mật khẩu 
        eye_NewPassword = driver.find_element(By.ID, "new-password-icon")
        eye_Confirm_NewPassword = driver.find_element(By.ID, "confirm-password-icon")
        eye_NewPassword.click()
        eye_Confirm_NewPassword.click()

        # Test nhập password và confirm password không khớp
        input_NewPassword.send_keys("12345")
        input_Confirm_NewPassword.send_keys("1234567")

        time.sleep(2)
        input_Confirm_NewPassword.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("Test nhập password và confirm password không khớp thành công")
        except:
            print("Không tìm thấy thông báo lỗi")

        time.sleep(3)
        # tìm lại nút nhập
        input_NewPassword = driver.find_element(By.ID, "id_new_password")
        input_Confirm_NewPassword = driver.find_element(By.ID, "id_confirm_new_password")
        # xem mật khẩu 
        eye_NewPassword = driver.find_element(By.ID, "new-password-icon")
        eye_Confirm_NewPassword = driver.find_element(By.ID, "confirm-password-icon")
        eye_NewPassword.click()
        eye_Confirm_NewPassword.click()

        # Test nhập password và confirm password khớp
        input_NewPassword.send_keys("1234567")
        input_Confirm_NewPassword.send_keys("1234567")
        time.sleep(2)
        input_Confirm_NewPassword.send_keys(Keys.RETURN)
        # Kiểm tra xem đã chuyển hướng đến trang OTP chưa
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Đăng nhập"))
            actualTitle = driver.title
            self.assertEqual(actualTitle, "Đăng nhập")
            print("Test nhập khớp password và confirm password thành công và chuyển hướng thành công")
        except:
            print("Test nhập khớp password và confirm password thất bại") 

        time.sleep(3)

        # đăng nhập bằng mật khẩu mới:
        inputUserName = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "id_password")
        eye_button = driver.find_element(By.ID, "new-password-icon")
        eye_button.click()
        inputUserName.send_keys("voduybao192005@gmail.com")
        password.send_keys("1234567")
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Trang Chủ"))
            actualTitle = driver.title
            print("Tiêu đề sau khi đăng nhập:", actualTitle)
            self.assertEqual(actualTitle, "Trang Chủ")
            print("Test đăng nhập thành công")
        except:
            print("Test đăng nhập thất bại")
        time.sleep(3)
        print("Kết thúc test quên mật khẩu")


if __name__ == "__main__":
    unittest.main()
