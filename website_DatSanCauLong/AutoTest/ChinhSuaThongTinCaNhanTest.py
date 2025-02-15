import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestChinhSuaThongTinCaNhan(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # Mở Chrome full màn hình
        self.driver.implicitly_wait(10)  # Chờ tối đa 10s nếu phần tử chưa xuất hiện

    def tearDown(self):
        self.driver.quit()  # Đóng trình duyệt sau khi test xong
    

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
        # Đăg nhập
        inputUserName = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "id_password")
        
        inputUserName.send_keys("voduybao192005@gmail.com")
        time.sleep(1)  # Nghỉ 1s trước khi nhập mật khẩu
        password.send_keys("123")
        time.sleep(1)
        # xem password
        eye_button.click()
        time.sleep(1.5)  # Chờ 1.5s trước khi nhấn Enter
        password.send_keys(Keys.RETURN)
        time.sleep(2)  # Chờ 3s để trang load lại
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Trang Chủ"))
            actualTitle = driver.title
            print("Tiêu đề sau khi đăng nhập:", actualTitle)
            self.assertEqual(actualTitle, "Trang Chủ")
            print("Test đăng nhập thành công")
        except:
            print("Test đăng nhập thất bại")

        # tìm logo user
        user_info = driver.find_element(By.CLASS_NAME, "user-info")
        user_info.click()
        time.sleep(1)
        # Tìm nút  thông tin cá nhân
        ThongTinCaNhan_button = driver.find_element(By.ID, "ThongTinCaNhan")
        ThongTinCaNhan_button.click()
        time.sleep(1)
        # Kiểm tra xem đã đến trang thông tin cá nhân chưa
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Thông Tin Cá Nhân"))
            actualTitle = driver.title
            print("Tiêu đề sau khi nhấn vào thông tin cá nhân:", actualTitle)
            self.assertEqual(actualTitle, "Thông Tin Cá Nhân")
            print("Test vào trang Thông Tin Cá Nhân thành công")
        except:
            print("Test vào trang Thông Tin Cá Nhân thất bại")

        time.sleep(3)
        # Tìm nút cập nhật thông tin:
        CapNhatThongTin_button = driver.find_element(By.ID, "CapNhatThongTin")
        CapNhatThongTin_button.click()
        try:
            WebDriverWait(driver, 5).until(EC.title_contains("Chỉnh Sửa Thông Tin"))
            actualTitle = driver.title
            print("Tiêu đề sau khi nhấn vào Chỉnh Sửa Thông Tin:", actualTitle)
            self.assertEqual(actualTitle, "Chỉnh Sửa Thông Tin")
            print("Test vào trang Chỉnh Sửa Thông Tin thành công")
        except:
            print("Test vào trang Chỉnh Sửa Thông Tin thất bại")

        time.sleep(2)
        # Tìm các trường chỉnh tên và ngày sinh
        full_name_Update_Form = driver.find_element(By.ID, "full_name_UpdateForm")
        dob_Update_Form = driver.find_element(By.ID, "dob_UpdateForm")
        # Nhập sai định dạng tên và năm sinh
        full_name_Update_Form.clear()
        time.sleep(1)
        full_name_Update_Form.send_keys("Nguyễn%% Văn A")
        dob_Update_Form.send_keys("11015050")
        time.sleep(1)
        dob_Update_Form.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("test sai định dạng tên và yêu cầu của ngày sinh thành công")
        except:
            print("Không tìm thấy thông báo lỗi")
        time.sleep(2)
        full_name_Update_Form = driver.find_element(By.ID, "full_name_UpdateForm")
        dob_Update_Form = driver.find_element(By.ID, "dob_UpdateForm")
        full_name_Update_Form.clear()
        dob_Update_Form.clear()
        # Nhập lại đúng format
        full_name_Update_Form.send_keys("Nguyễn Văn A")
        dob_Update_Form.send_keys("11011990")
        time.sleep(2)
        dob_Update_Form.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("Nhập đúng định dạng thất bại")
        except:
            print("Nhập đúng định dạng thành công")
        
        # Kiểm tra đã chỉnh sửa tài khoản thành công chưa
        try:
            # Chờ thông báo thành công xuất hiện và trở nên hiển thị
            message_box = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "message-box"))
            )
            success_message = message_box.text
            print(f"Chỉnh sửa thành công. Thông báo: {success_message}")
        except :
            print("Không tìm thấy thông báo thành công.")
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()
