import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait,Select
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
        account_manage_link = driver.find_element(By.LINK_TEXT, "Quản lý tài khoản")
        account_manage_link.click()
        print("Nhấn menu và chức năng quản lí tài khoản thành công")
        try:    
            WebDriverWait(driver, 5).until(EC.title_contains("Quản lý tài khoản"))
            actualTitle = driver.title
            print("Tiêu đề sau khi nhấn vào Quản lý tài khoản:", actualTitle)
            self.assertEqual(actualTitle, "Quản lý tài khoản")
            print("Test vào trang Quản lý tài khoản thành công")
        except:
            print("Test vào trang Quản lý tài khoản thất bại")
        time.sleep(1)

        # Tổng quan trang quản lí tài khoản
        # Cuộn từ từ xuống dưới
        print("Cuộn từ từ xuống dưới...")
        self.scroll_smoothly(driver, target_position=1500, step=50, delay=0.05)

        # Cuộn từ từ lên trên
        print("Cuộn từ từ lên trên...")
        self.scroll_smoothly(driver, target_position=0, step=50, delay=0.05)
        time.sleep(1)

        # TEST CHỨC NĂNG THÊM 1 TÀI KHOẢN MỚI
        # Tìm nơi nhập các thông tin của tài khoản:
        username_add_account = driver.find_element(By.ID, "username_add_account")
        password_add_account = driver.find_element(By.ID, "password_add_account")
        role = driver.find_element(By.ID, "role")
        # Test nhập thiếu trường
        username_add_account.send_keys("testuser02@gmail.com")
        role.click()
        # Chọn vai trò từ dropdown
        select_role = Select(role)  # Tạo đối tượng Select từ thẻ <select>
        select_role.select_by_visible_text("Người dùng")
        username_add_account.send_keys(Keys.RETURN)
        time.sleep(1)

        # Nhập sai định dạng
        username_add_account.clear()
        username_add_account.send_keys("testuser02@gmai")
        password_add_account.send_keys("pass2")
        print("Nhập đầy đủ thông tin")
        time.sleep(2)
        password_add_account.send_keys(Keys.RETURN)
        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-list"))
            )
            print("test sai định dạng email thành công")
        except:
            print("Không tìm thấy thông báo lỗi")
        time.sleep(2.5)

        # Nhập đúng toàn bộ thông tin:
        username_add_account = driver.find_element(By.ID, "username_add_account")
        password_add_account = driver.find_element(By.ID, "password_add_account")
        username_add_account.clear()
        username_add_account.send_keys("testuser02@gmail.com")
        password_add_account.send_keys("pass2")
        time.sleep(2.5)
        password_add_account.send_keys(Keys.RETURN)
        # kiểm tra có thông báo không
        try:
            # Chờ phần tử chứa messages xuất hiện
            messages_container = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "messages"))
            )
            # Lấy tất cả các message bên trong
            messages = messages_container.find_elements(By.CLASS_NAME, "message")

            # Lặp qua từng thông báo
            for message in messages:
                message_class = message.get_attribute("class")  # Lấy class của thông báo
                message_text = message.text  # Lấy nội dung thông báo
                if "success" in message_class:
                    print("Test thêm tài khoản thành công")
                    print(f"Success message: {message_text}")
                elif "error" in message_class:
                    print("Test thêm tài khoản thất bại")
                    print(f"Error message: {message_text}")
        except Exception as e:
            print(f"Không tìm thấy thông báo. Lỗi: {str(e)}")
        time.sleep(2)
        # kéo xuống dưới
        # Cuộn từ từ xuống dưới
        print("Cuộn từ từ xuống dưới...")
        self.scroll_smoothly(driver, target_position=1300, step=50, delay=0.05)
        time.sleep(2)
        # TEST CHỨC NĂNG CHỈNH SỬA 1 TÀI KHOẢN
        # Tìm nút chỉnh sửa tài khoản
        # Tìm dựa trên user muốn sửa 
        username = "testuser02@gmail.com"
        row = driver.find_element(By.XPATH, f"//td[text()='{username}']/..")  # Tìm hàng chứa username
        edit_button = row.find_element(By.XPATH, ".//button[contains(@class, 'edit-btn')]")  # Tìm nút "Chỉnh sửa" trong hàng
        edit_button.click()
        # Đợi form chỉnh sửa hiển thị
        edit_form = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//tr[contains(@id, 'editRow') and not(contains(@class, 'hidden'))]"))
        )
        time.sleep(1)
       
        # Điền mật khẩu mới
        new_password = edit_form.find_element(By.ID, "change_password")
        new_password.send_keys("12345")  # Mật khẩu mới

        # Chọn vai trò từ dropdown
        role_dropdown2 = edit_form.find_element(By.ID, "role2")
        select_role2 = Select(role_dropdown2)  # Tạo đối tượng Select từ thẻ <select>
        select_role2.select_by_visible_text("Staff")  # Chọn "Quản trị viên"
        time.sleep(1.5)
        # Tìm nút cập nhật
        # 4. Tìm nút "Cập nhật" trong form chỉnh sửa
        update_button = edit_form.find_element(By.XPATH, ".//button[contains(text(), 'Cập nhật')]")
        print("tìm thấy nút cập nhật")
        # 5. Nhấn vào nút "Cập nhật"
        update_button.click()
        # Xử lý thông báo JS nếu xuất hiện
        time.sleep(5)
        try:
            alert = driver.switch_to.alert
            alert_message = alert.text
            print("Cập nhật tài khoản thành công")
            print("Thông báo từ JS:", alert_message)
            time.sleep(2)
            alert.accept()
        except :
            print("Không có thông báo JS nào xuất hiện.")
        
        time.sleep(6)

        # TEST CHỨC NĂNG XÓA TÀI KHOẢN 
        # Tìm nút xóa
        row = driver.find_element(By.XPATH, f"//td[text()='{username}']/..")  # Tìm hàng chứa username
        edit_button = row.find_element(By.XPATH, ".//button[contains(@class, 'delete-btn')]")  # Tìm nút "Chỉnh sửa" trong hàng
        print("Tìm thấy nút xóa")
        edit_button.click()
        # 3. Đợi modal xác nhận xóa xuất hiện
        delete_modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "deleteConfirmModal"))
        )
        time.sleep(3)
        # 4. Tìm và nhấn nút "Xác nhận" trong modal
        confirm_delete_button = delete_modal.find_element(By.XPATH, ".//button[contains(@class, 'confirm-delete')]")
        print("Tìm thấy nút xác nhận xóa")
        confirm_delete_button.click()
        time.sleep(4)
        try:
            alert = driver.switch_to.alert
            alert_message = alert.text
            print("Xóa tài khoản thành công")
            print("Thông báo từ JS:", alert_message)
            time.sleep(2)
            alert.accept()
        except :
            print("Không có thông báo JS nào xuất hiện.")
        
        time.sleep(6)
        

if __name__ == "__main__":
    unittest.main()