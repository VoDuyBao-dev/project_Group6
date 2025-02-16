import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestUnitManageCourt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Khởi tạo trình duyệt trước khi chạy test"""
        service = Service(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=service)
        cls.browser.implicitly_wait(10)  # Đợi tối đa 10s nếu phần tử chưa load

    @classmethod
    def tearDownClass(cls):
        """Đóng trình duyệt sau khi chạy xong tất cả test"""
        cls.browser.quit()

    def test_unit_manager_san_page_loads(self):
        """Test: Kiểm tra trang danh sách sân hiển thị đúng không"""
        self.browser.get("http://127.0.0.1:8000/manager_san/")  # Mở trang quản lý sân
        time.sleep(2)

        # Kiểm tra tiêu đề trang
        self.assertIn("Quản lý thông tin sân", self.browser.title)

        # Kiểm tra trang có hiển thị danh sách sân không
        heading = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(heading, "Danh sách các sân")

    def test_unit_edit_court_info(self):
        """Test: Chỉnh sửa thông tin sân và lưu thay đổi"""
        self.browser.get("http://127.0.0.1:8000/manager_san/")
        time.sleep(2)

        # Nhấn vào nút "Chỉnh sửa"
        edit_buttons = self.browser.find_elements(By.XPATH, "//button[contains(text(), 'Chỉnh sửa')]")
        if not edit_buttons:
            self.fail("Không tìm thấy nút Chỉnh sửa")
        edit_buttons[0].click()
        time.sleep(2)

        # Chỉnh sửa thông tin sân
        name_input = self.browser.find_element(By.NAME, "name")
        name_input.clear()
        name_input.send_keys("Court A123 - Updated")

        # Chọn tên chi nhánh mới từ dropdown
        branch_select = Select(self.browser.find_element(By.NAME, "badminton_hall"))
        branch_select.select_by_index(4)  # Chọn chi nhánh thứ 4

        # Chọn trạng thái mới từ dropdown
        status_select = Select(self.browser.find_element(By.NAME, "status"))
        status_select.select_by_index(2)  # Chọn trạng thái mới

        # # (Tùy chọn) Upload ảnh mới nếu cần
        # image_input = self.browser.find_element(By.NAME, "image")
        # image_input.send_keys("C:\Users\Minh Chau\Pictures\Screenshots\Screenshot 2024-05-22 075849.png")

        # Nhấn "Lưu thay đổi"
        save_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Lưu thay đổi')]")
        save_button.click()
        time.sleep(3)

        # Kiểm tra xem có thông báo thành công không
        success_message = self.browser.find_element(By.CLASS_NAME, "alert-success")
        self.assertTrue(success_message.is_displayed(), "Cập nhật sân thất bại")
    
def test_unit_delete_court(self):
        """Test: Xóa sân và kiểm tra kết quả"""
        self.browser.get("http://127.0.0.1:8000/manager_san/")
        time.sleep(2)

        # Nhấn vào nút "Xóa" để mở modal xác nhận
        delete_buttons = self.browser.find_elements(By.XPATH, "//button[contains(text(), 'Xóa')]")
        if not delete_buttons:
            self.fail("Không tìm thấy nút Xóa")
        delete_buttons[0].click()
        time.sleep(2)

        # Nhấn vào nút "Xóa" trong modal xác nhận
        confirm_delete_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Xóa')]")
        confirm_delete_button.click()
        time.sleep(3)

        # Kiểm tra xem có thông báo thành công không
        success_message = self.browser.find_element(By.CLASS_NAME, "alert-success")
        self.assertTrue(success_message.is_displayed(), "Xóa sân thất bại")


if __name__ == "__main__":
    unittest.main()
