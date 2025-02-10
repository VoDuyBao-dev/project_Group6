import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestUserSignIn(unittest.TestCase):
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
        # Tìm nút xem mật khẩu
        eye_button = driver.find_element(By.ID, "new-password-icon")
        # Nhập sai định dạng tên tài khoản
        inputUserName = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "id_password")
        
        inputUserName.send_keys("voduybao1905200gmail")
        time.sleep(1)  # Nghỉ 1s trước khi nhập mật khẩu
        password.send_keys("12345")
        time.sleep(1)
        # xem password
        eye_button.click()
        time.sleep(1.5)  # Chờ 1.5s trước khi nhấn Enter
        password.send_keys(Keys.RETURN)
        time.sleep(3)  # Chờ 3s để trang load lại

        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("Đăng nhập sai định dạng tài khoản")
        except:
            print("Không tìm thấy thông báo lỗi")
            
        # Test đăng nhập sai 5 lần
        #  Cần tìm lại phần tử sau khi trang load lại
        inputUserName = self.driver.find_element(By.ID, "username")
        inputUserName.clear()
        inputUserName.send_keys("voduybao192005@gmail.com")
        for i in range(5):
            self.enter_credentials("123444")
            self.check_error_message(".alert.alert-danger", i+1)
            time.sleep(2)  # Chờ 2s để trang load lại

         
        # test đăng nhập đúng
        # Tìm lại phần tử:
        self.enter_credentials("1234")
        self.check_error_message("alert.alert-danger",6)
            
        # Kiểm tra xem đăng nhập có thành công không
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Trang Chủ"))
            actualTitle = driver.title
            print("Tiêu đề sau khi đăng nhập:", actualTitle)
            self.assertEqual(actualTitle, "Trang Chủ")
            print("Test đăng nhập thành công")
        except:
            print("Test đăng nhập thất bại")

        # đăng xuất để test chức năng nhớ tài khoản
        user_info = driver.find_element(By.CLASS_NAME, "user-info")
        user_info.click()
        time.sleep(0.5)
        logout_button = driver.find_element(By.ID, "logout")
        # Nhấn vào nút "Đăng xuất"
        logout_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi chuyển trang

        try:
            # Đợi phần tử đặc trưng của trang chủ khi chưa đăng nhập xuất hiện
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.login-btn")))
            print("Đã nhấn vào nút Đăng xuất và chuyển hướng đến đăng nhập thành công.")
        except:
            print("Test đăng xuất thất bại")

        # Nhấn đăng nhập lại
        SignIn_button = driver.find_element(By.CSS_SELECTOR, ".btn.login-btn")  
        SignIn_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi chuyển trang

        # Kiểm tra kết quả
        self.assertIn("Đăng nhập", driver.title)  
        print("Đã nhấn vào nút Đăng nhập và chuyển hướng thành công.")
        inputUserName = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "id_password")
        # Tìm nút nhớ tài khoản và xem mật khẩu
        remember_button = driver.find_element(By.ID, "remember")
        eye_button = driver.find_element(By.ID, "new-password-icon")
        # Nhấn nhớ tài khoản
        remember_button.click()
        print("Nhấn nhớ tài khoản thành công")
        time.sleep(2)
        inputUserName.send_keys("voduybao192005@gmail.com")
        password.send_keys("1234")
        # xem password
        eye_button.click()
        time.sleep(1.5) 
        password.send_keys(Keys.RETURN)
        # Kiểm tra xem đăng nhập có thành công không
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Trang Chủ"))
            actualTitle = driver.title
            print("Tiêu đề sau khi đăng nhập:", actualTitle)
            self.assertEqual(actualTitle, "Trang Chủ")
            print("Test đăng nhập thành công")
        except:
            print("Test đăng nhập thất bại")
        
        time.sleep(1)
        # tìm lại nút đăng xuất khi tải trang mớimới
        user_info = driver.find_element(By.CLASS_NAME, "user-info")
        user_info.click()
        time.sleep(0.5)
        logout_button = driver.find_element(By.ID, "logout")
        # Nhấn vào nút "Đăng xuất"
        logout_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi chuyển trang
        try:
            # Đợi phần tử đặc trưng của trang chủ khi chưa đăng nhập xuất hiện
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.login-btn")))
            print("Đã nhấn vào nút Đăng xuất và chuyển hướng đến đăng nhập thành công.")
        except:
            print("Test đăng xuất thất bại")

        time.sleep(1)
        SignIn_button = driver.find_element(By.CSS_SELECTOR, ".btn.login-btn")  
        SignIn_button.click()
        time.sleep(2)  # Chờ 2 giây sau khi chuyển trang
        self.assertIn("Đăng nhập", driver.title)  # Kiểm tra xem tiêu đề có đúng là trang đăng nhập không
        # In kết quả ra terminal
        print("Đã nhấn vào nút Đăng nhập và chuyển hướng thành công.")
         

if __name__ == "__main__":
    unittest.main()
