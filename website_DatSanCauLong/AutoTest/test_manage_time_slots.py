#  Các Trường Hợp Kiểm Thử
# Nhập đầy đủ thông tin hợp lệ →  Thêm lịch thành công.
# Nhập thiếu một hoặc nhiều trường →  Hiển thị lỗi.
# Nhập trùng ngày & khung giờ →  Hiển thị lỗi.
# Nhập giá không hợp lệ (chữ thay vì số) →  Hiển thị lỗi.
# Xóa lịch đã tạo →  Lịch bị xóa thành công.





import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ManageTimeSlotsTest(unittest.TestCase):

    def setUp(self):
        """Khởi động trình duyệt trước mỗi test"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/admin/login/")  # URL trang admin

        # Đăng nhập Admin trước khi test
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        username.send_keys("admin")
        password.send_keys("123456")  # Đổi thành mật khẩu admin của bạn
        password.send_keys(Keys.RETURN)
        time.sleep(2)  # Chờ tải trang

        # Chuyển đến trang quản lý time slots
        self.driver.get("http://127.0.0.1:8000/manage_time_slots/")
        time.sleep(2)

    def tearDown(self):
        """Đóng trình duyệt sau mỗi test"""
        self.driver.quit()

    def test_add_valid_time_slot(self):
        """Test thêm lịch hợp lệ"""
        driver = self.driver

        # Chọn ngày trong tuần
        day_of_week = driver.find_element(By.NAME, "day_of_week")
        day_of_week.send_keys("Thứ 2")

        # Nhập khung giờ
        time_frame = driver.find_element(By.NAME, "time_frame")
        time_frame.send_keys("08h - 10h")

        # Nhập giá tiền
        driver.find_element(By.NAME, "fixed_price").send_keys("200000")
        driver.find_element(By.NAME, "daily_price").send_keys("180000")
        driver.find_element(By.NAME, "flexible_price").send_keys("150000")

        # Chọn trạng thái
        status = driver.find_element(By.NAME, "status")
        status.send_keys("Hoạt động")

        # Nhấn nút Lưu
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Kiểm tra thông báo thành công
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        success = any("Thêm lịch và giá thành công." in message.text for message in messages)
        self.assertTrue(success, "Không thấy thông báo thành công!")

    def test_add_time_slot_missing_fields(self):
        """Test nhập thiếu dữ liệu"""
        driver = self.driver

        # Chỉ chọn ngày trong tuần
        day_of_week = driver.find_element(By.NAME, "day_of_week")
        day_of_week.send_keys("Thứ 3")

        # Nhấn nút Lưu mà không nhập gì thêm
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Kiểm tra thông báo lỗi
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        error = any("Vui lòng nhập đầy đủ thông tin!" in message.text for message in messages)
        self.assertTrue(error, "Không thấy thông báo lỗi khi nhập thiếu thông tin!")

    def test_add_duplicate_time_slot(self):
        """Test nhập trùng ngày & giờ"""
        driver = self.driver

        # Chọn ngày trong tuần
        day_of_week = driver.find_element(By.NAME, "day_of_week")
        day_of_week.send_keys("Thứ 2")

        # Nhập khung giờ trùng với lịch đã tồn tại
        time_frame = driver.find_element(By.NAME, "time_frame")
        time_frame.send_keys("08h - 10h")

        # Nhập giá tiền
        driver.find_element(By.NAME, "fixed_price").send_keys("200000")
        driver.find_element(By.NAME, "daily_price").send_keys("180000")
        driver.find_element(By.NAME, "flexible_price").send_keys("150000")

        # Chọn trạng thái
        status = driver.find_element(By.NAME, "status")
        status.send_keys("Hoạt động")

        # Nhấn nút Lưu
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Kiểm tra thông báo lỗi trùng lịch
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        error = any("Trùng ngày và khung giờ" in message.text for message in messages)
        self.assertTrue(error, "Không thấy thông báo lỗi khi nhập trùng lịch!")

    def test_add_time_slot_invalid_price(self):
        """Test nhập giá không hợp lệ"""
        driver = self.driver

        # Chọn ngày trong tuần
        day_of_week = driver.find_element(By.NAME, "day_of_week")
        day_of_week.send_keys("Thứ 4")

        # Nhập khung giờ
        time_frame = driver.find_element(By.NAME, "time_frame")
        time_frame.send_keys("10h - 12h")

        # Nhập giá không hợp lệ (chữ thay vì số)
        driver.find_element(By.NAME, "fixed_price").send_keys("hai trăm nghìn")
        driver.find_element(By.NAME, "daily_price").send_keys("180000")
        driver.find_element(By.NAME, "flexible_price").send_keys("150000")

        # Chọn trạng thái
        status = driver.find_element(By.NAME, "status")
        status.send_keys("Hoạt động")

        # Nhấn nút Lưu
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Kiểm tra thông báo lỗi
        messages = driver.find_elements(By.CLASS_NAME, "messages")
        error = any("Vui lòng nhập giá hợp lệ!" in message.text for message in messages)
        self.assertTrue(error, "Không thấy thông báo lỗi khi nhập giá không hợp lệ!")

    def test_delete_time_slot(self):
        """Test xóa lịch đã tạo"""
        driver = self.driver

        # Xóa lịch đầu tiên trong danh sách nếu có
        delete_buttons = driver.find_elements(By.XPATH, "//a[contains(text(),'Xóa')]")
        if delete_buttons:
            delete_buttons[0].click()
            time.sleep(2)

            # Kiểm tra xem có còn nút xóa không
            new_delete_buttons = driver.find_elements(By.XPATH, "//a[contains(text(),'Xóa')]")
            self.assertTrue(len(new_delete_buttons) < len(delete_buttons), "Lịch không bị xóa!")
        else:
            self.skipTest("Không có lịch nào để xóa!")

if __name__ == "__main__":
    unittest.main()
