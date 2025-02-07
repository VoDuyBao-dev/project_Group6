import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestUserSearchCourt(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # Mở Chrome full màn hình
        self.driver.implicitly_wait(10)  # Chờ tối đa 10s nếu phần tử chưa xuất hiện

    def tearDown(self):
        self.driver.quit()  # Đóng trình duyệt sau khi test xong

    def scroll_smoothly(self, driver, direction="down", step=100, delay=0.05):
    
        if direction == "down":
            # Lấy chiều cao của trang
            total_height = driver.execute_script("return document.body.scrollHeight")
            current_position = 0

            while current_position < total_height:
                current_position += step
                driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(delay)
        elif direction == "up":
            # Lấy vị trí hiện tại (đang ở cuối trang)
            current_position = driver.execute_script("return window.scrollY")

            while current_position > 0:
                current_position -= step
                driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(delay)

    def test_user_SignIn(self):
        print("Bắt đầu kiểm thử tìm sân cầu lông")
        driver = self.driver
        driver.get("http://127.0.0.1:8000")
        time.sleep(2)  
        
        

        # Cuộn từ từ xuống dưới
        print("Cuộn từ từ xuống dưới...")
        self.scroll_smoothly(driver, direction="down", step=100, delay=0.05)

        # Cuộn từ từ lên trên
        print("Cuộn từ từ lên trên...")
        self.scroll_smoothly(driver, direction="up", step=100, delay=0.05)

        # Tìm nút đặt sân:
        DatSan_Button = driver.find_element(By.ID, "DatSan_button")  
        time.sleep(1)
        DatSan_Button.click()
        time.sleep(1)
        # cuộn để xem trang
        self.scroll_smoothly(driver, direction="down", step=100, delay=0.05)
        self.scroll_smoothly(driver, direction="up", step=100, delay=0.05)
        time.sleep(1)
        # Tìm nút nhập tìm kiếm sân
        search_court = driver.find_element(By.ID, "search_query")  
        # Nhập nội dung tìm kiếm: Đường
        search_court.send_keys("đường A")
        time.sleep(1)
        search_court.send_keys(Keys.RETURN)
        time.sleep(3)
        print("test tìm sân ở Đường A hoàn tất")

        # Nhập nội dung tìm kiếm: Quận
        search_court = driver.find_element(By.ID, "search_query") 
        search_court.clear()
        search_court.send_keys("quận J")
        time.sleep(1)
        search_court.send_keys(Keys.RETURN)
        time.sleep(3)
        print("test tìm sân ở quận hoàn tất")

        # Nhập nội dung tìm kiếm: Tìm 1 đường hoặc quận không có trong danh sách
        search_court = driver.find_element(By.ID, "search_query") 
        search_court.clear()
        search_court.send_keys("đường yyyy, quận zzzzzz")
        time.sleep(1)
        search_court.send_keys(Keys.RETURN)
        time.sleep(3)
        print("test tìm sân ở đường hoặc quận không có trong danh sách hoàn tất")



if __name__ == "__main__":
    unittest.main()