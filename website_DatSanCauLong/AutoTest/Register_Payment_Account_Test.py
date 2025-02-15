import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class TestUserSearchCourt(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  
        self.driver.implicitly_wait(10)  

    def tearDown(self):
        self.driver.quit()  

    def scroll_smoothly(self, driver, direction="down", step=100, delay=0.05, target_position=None):
    
        if target_position is not None:
            # Cuộn đến vị trí cụ thể
            current_position = driver.execute_script("return window.scrollY")

            if current_position < target_position:
                # Cuộn xuống
                while current_position < target_position:
                    current_position += step
                    if current_position > target_position:
                        current_position = target_position
                    driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(delay)
            elif current_position > target_position:
                # Cuộn lên
                while current_position > target_position:
                    current_position -= step
                    if current_position < target_position:
                        current_position = target_position
                    driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(delay)
        else:
            # Cuộn dựa trên hướng nếu target_position không được đặt
            if direction == "down":
                total_height = driver.execute_script("return document.body.scrollHeight")
                current_position = driver.execute_script("return window.scrollY")

                while current_position < total_height:
                    current_position += step
                    driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(delay)
            elif direction == "up":
                current_position = driver.execute_script("return window.scrollY")

                while current_position > 0:
                    current_position -= step
                    driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(delay)

    def test_user_SignIn(self):
        print("Bắt đầu kiểm thử đăng ký tài khoản thanh toán")
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
        # Đăg nhập
        inputUserName = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "id_password")
        
        inputUserName.send_keys("voduybao19052005@gmail.com")
        time.sleep(1)  # Nghỉ 1s trước khi nhập mật khẩu
        password.send_keys("123")
        time.sleep(1)
        # xem password
        eye_button.click()
        time.sleep(1.5)  # Chờ 1.5s trước khi nhấn Enter
        password.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Trang Chủ"))
            actualTitle = driver.title
            print("Tiêu đề sau khi đăng nhập:", actualTitle)
            self.assertEqual(actualTitle, "Trang Chủ")
            print("Test đăng nhập thành công")
        except:
            print("Test đăng nhập thất bại")
        time.sleep(2)  # Chờ 2s để trang load lại

        # Cuộn từ từ xuống dưới
        print("Cuộn từ từ xuống dưới...")
        self.scroll_smoothly(driver, target_position=2000, step=50, delay=0.05)

        # Cuộn từ từ lên trên
        print("Cuộn từ từ lên trên...")
        self.scroll_smoothly(driver, target_position=0, step=50, delay=0.05)
        time.sleep(1)

        # Tìm menu
        menu_button = driver.find_element(By.ID, "btn")
        menu_button.click()
        time.sleep(2)
        # Tìm nút quản lí tài khoản
        account_manage_link = driver.find_element(By.LINK_TEXT, "Quản lý sân")
        account_manage_link.click()
        print("Nhấn menu và chức năng Quản lý sân thành công")
        time.sleep(1)
        # Tìm chức năng thêm tài khảon thanh toán
        DangKyTaiKhoanThanhToan_link = driver.find_element(By.LINK_TEXT, "Thêm tài khoản thanh toán")
        DangKyTaiKhoanThanhToan_link.click()
        try:    
            WebDriverWait(driver, 5).until(EC.title_contains("Đăng ký tài khoản thanh toán"))
            actualTitle = driver.title
            print("Tiêu đề sau khi nhấn vào Đăng ký tài khoản thanh toán:", actualTitle)
            self.assertEqual(actualTitle, "Đăng ký tài khoản thanh toán")
            print("Test vào trang Đăng ký tài khoản thanh toán thành công")
        except:
            print("Test vào trang Đăng ký tài khoản thanh toán thất bại")
        time.sleep(3)
    
        # Tìm nút nhập các thông tin:
        account_Holder = driver.find_element(By.ID, "accountHolder")  
        account_Number = driver.find_element(By.ID, "accountNumber")

        # Nhập thiếu trường
        account_Holder.send_keys("NGuyen Văn A")
        account_Holder.send_keys(Keys.RETURN)
        time.sleep(2)

        # Nhập sai định dạng tên và số tài khoản khi chọn phương thức ngân hàng:
        account_Number.send_keys("1234")
        # Tìm nút chọn phương thức
        # Tìm dropdown bằng ID
        payment_method = Select(driver.find_element(By.ID, "id_paymentMethod"))

        # Chọn phương thức thanh toán bằng value
        payment_method.select_by_value("bank")
        print("chọn phương thức: Ngân hàng thành công")
        time.sleep(2)
        account_Number.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("test Nhập sai định dạng tên và số tài khoản khi chọn phương thức ngân hàng thành công")
        except:
            print("Không tìm thấy thông báo lỗi")
        time.sleep(5)

        # Nhập sai định dạng tên và số tài khoản khi chọn phương thức Momo:
        account_Holder = driver.find_element(By.ID, "accountHolder")  
        account_Number = driver.find_element(By.ID, "accountNumber")
        account_Holder.clear()
        account_Number.clear()
        account_Holder.send_keys("Nguy% Van A")
        account_Number.send_keys("12345678")

        payment_method = Select(driver.find_element(By.ID, "id_paymentMethod"))
        payment_method.select_by_value("momo")
        print("chọn phương thức: Momo thành công")
        time.sleep(2)
        account_Number.send_keys(Keys.RETURN)

        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("test Nhập sai định dạng tên và số tài khoản khi chọn phương thức Momo thành công")
        except:
            print("Không tìm thấy thông báo lỗi")
        time.sleep(5)

        # Nhập trùng số tài khoản đã đăng ký
        account_Holder = driver.find_element(By.ID, "accountHolder")  
        account_Number = driver.find_element(By.ID, "accountNumber")
        account_Holder.clear()
        account_Number.clear()
        account_Holder.send_keys("NGUYEN VAN A")
        account_Number.send_keys("12312323312")

        payment_method = Select(driver.find_element(By.ID, "id_paymentMethod"))
        payment_method.select_by_value("bank")
        print("chọn phương thức: Ngân hàng thành công")
        time.sleep(2)
        account_Number.send_keys(Keys.RETURN)

        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("test Nhập trùng số tài khoản đã đăng ký thành công")
        except:
            print("Không tìm thấy thông báo lỗi")
        time.sleep(5)

        # Nhập đúng
        account_Number = driver.find_element(By.ID, "accountNumber")
        account_Number.clear()
        account_Number.send_keys("1234567899")
        time.sleep(2)
        account_Number.send_keys(Keys.RETURN)

        try:
            # Chờ thông báo thành công xuất hiện và trở nên hiển thị
            message_box = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "message-box"))
            )
            success_message = message_box.text
            print(f"Đăng ký thành công. Thông báo: {success_message}")
        except :
            print("Không tìm thấy thông báo thành công.")

        time.sleep(3)
      
if __name__ == "__main__":
    unittest.main()