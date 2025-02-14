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

    def test_user_SignIn(self):
        print("Bắt đầu kiểm thử đăng ký tài khoản thanh toán")
        driver = self.driver
        driver.get("http://127.0.0.1:8000/DangKyTaiKhoanThanhToan")
        time.sleep(2)  
        
    
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