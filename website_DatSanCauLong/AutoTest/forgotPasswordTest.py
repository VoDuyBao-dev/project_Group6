import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



class TestUserForgotPassword(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
        print("Bắt đầu kiểm thử đăng nhập sân cầu lông")
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
        # inputUserName = driver.find_element(By.ID, "username")
        # password = driver.find_element(By.ID, "id_password")
        
        # inputUserName.send_keys("voduybao192005@gmail.com")
        # time.sleep(1)  # Nghỉ 1s trước khi nhập mật khẩu
        # for i in range(5):
        #     # Tìm nút xem mật khẩu
        #     eye_button = driver.find_element(By.ID, "new-password-icon")
        #     eye_button.click()
        #     self.enter_credentials("123444")
        #     self.check_error_message(".alert.alert-danger", i+1)
        #     time.sleep(2)  # Chờ 2s để trang load lại
        
        # time.sleep(3)

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
        # đã đến đoạn nhập email chưa tồn tại


        







if __name__ == "__main__":
    unittest.main()
