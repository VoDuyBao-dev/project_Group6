








import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ManageCourtTest(unittest.TestCase):
    
    def setUp(self):
        """Khởi động trình duyệt trước mỗi test"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/admin/login/")  # URL trang admin
        
        # Đăng nhập Admin
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        username.send_keys("admin")
        password.send_keys("123456")  # Đổi thành mật khẩu admin của bạn
        password.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # Chuyển đến trang quản lý sân
        self.driver.get("http://127.0.0.1:8000/manage_courts/")
        time.sleep(2)

    def tearDown(self):
        """Đóng trình duyệt sau mỗi test"""
        self.driver.quit()

    def test_add_court(self):
        """Test thêm sân mới"""
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "add-court-btn").click()
        time.sleep(2)
        
        # Điền thông tin sân
        name_field = driver.find_element(By.NAME, "name")
        name_field.send_keys("Sân Test")
        
        # Chọn chi nhánh
        branch_field = driver.find_element(By.NAME, "badminton_hall")
        branch_field.send_keys("Chi nhánh A")
        
        # Chọn trạng thái
        status_field = driver.find_element(By.NAME, "status")
        status_field.send_keys("empty")
        
        # Nhấn nút Lưu
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Kiểm tra thông báo thành công
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        success = any("Sân đã được thêm thành công" in message.text for message in messages)
        self.assertTrue(success, "Không thấy thông báo thành công khi thêm sân!")

    def test_edit_court(self):
        """Test chỉnh sửa sân"""
        driver = self.driver
        
        # Chọn sân đầu tiên để chỉnh sửa
        edit_buttons = driver.find_elements(By.CLASS_NAME, "edit-btn")
        if not edit_buttons:
            self.skipTest("Không có sân nào để chỉnh sửa!")
        edit_buttons[0].click()
        time.sleep(2)
        
        # Thay đổi tên sân
        name_field = driver.find_element(By.NAME, "name")
        name_field.clear()
        name_field.send_keys("Sân Đã Sửa")
        
        # Lưu thay đổi
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Kiểm tra thông báo thành công
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        success = any("Thông tin sân đã được cập nhật thành công!" in message.text for message in messages)
        self.assertTrue(success, "Không thấy thông báo thành công khi chỉnh sửa sân!")
    
    def test_delete_court(self):
        """Test xóa sân"""
        driver = self.driver
        
        # Chọn sân đầu tiên để xóa
        delete_buttons = driver.find_elements(By.CLASS_NAME, "delete-btn")
        if not delete_buttons:
            self.skipTest("Không có sân nào để xóa!")
        delete_buttons[0].click()
        time.sleep(2)
        
        # Xác nhận xóa
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        
        # Kiểm tra thông báo xóa thành công
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        success = any("Sân đã được xóa thành công!" in message.text for message in messages)
        self.assertTrue(success, "Không thấy thông báo thành công khi xóa sân!")

if __name__ == "__main__":
    unittest.main()
