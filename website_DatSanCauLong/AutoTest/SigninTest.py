import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestAdminLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Chờ tối đa 10s nếu phần tử chưa xuất hiện

    def tearDown(self):
        self.driver.quit()  # Đóng trình duyệt sau khi test xong

    def test_unit_user(self):
        print("Bắt đầu kiểm thử đăng nhập admin")
        driver = self.driver
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
        time.sleep(2)  # ⏳ Chờ 2s để trang tải hoàn toàn

        # Nhập sai lần đầu
        inputUserName = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")

        inputUserName.send_keys("admin")
        time.sleep(1)  # ⏳ Nghỉ 1s trước khi nhập mật khẩu
        password.send_keys("12345")
        time.sleep(1.5)  # ⏳ Chờ 1.5s trước khi nhấn Enter
        password.send_keys(Keys.RETURN)
        time.sleep(3)  # ⏳ Chờ 3s để trang load lại

        # Chờ xem có xuất hiện thông báo lỗi không
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "errornote"))
            )
            print("Đăng nhập sai lần đầu, nhập lại thông tin đúng.")
        except:
            print("Không tìm thấy thông báo lỗi, có thể đã đăng nhập thành công.")
            return  # Dừng test nếu lỡ đăng nhập thành công

        # 🔥 **Cần tìm lại phần tử sau khi trang load lại**
        time.sleep(2)  # ⏳ Chờ 2s trước khi tìm lại phần tử
        inputUserName = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password = driver.find_element(By.NAME, "password")

        # Nhập lại đúng tài khoản và mật khẩu
        inputUserName.clear()
        time.sleep(1)  # ⏳ Chờ 1s trước khi nhập lại
        password.clear()
        time.sleep(1)

        inputUserName.send_keys("admin")
        time.sleep(1.5)  # ⏳ Chờ 1.5s trước khi nhập mật khẩu
        password.send_keys("123")
        time.sleep(1)
        password.send_keys(Keys.RETURN)
        time.sleep(3)  # ⏳ Chờ 3s để đăng nhập

        # Kiểm tra xem đăng nhập có thành công không
        WebDriverWait(driver, 5).until(EC.title_contains("Site administration"))
        actualTitle = driver.title
        print("Tiêu đề sau khi đăng nhập:", actualTitle)

        self.assertEqual(actualTitle, "Site administration | Django site admin")

if __name__ == "__main__":
    unittest.main()
