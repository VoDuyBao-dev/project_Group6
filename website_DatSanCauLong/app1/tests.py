from django.test import TestCase
from django.urls import reverse
from app1.models import Booking
from datetime import date, time

class BookingTestCase(TestCase):
    def setUp(self):
        """Tạo dữ liệu mẫu cho test"""
        self.booking_data = {
            "scheduleType": "fixed",
            "date": "2025-02-10",
            "time": "14:00",
        }

    def test_booking_page_loads(self):
        """Kiểm tra trang booking có load thành công không"""
        response = self.client.get(reverse('booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/booking.html')

    def test_successful_booking(self):
        """Kiểm tra đặt sân thành công"""
        response = self.client.post(reverse('booking'), self.booking_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Booking.objects.filter(date="2025-02-10", time="14:00").exists())
        self.assertContains(response, "Đặt lịch thành công")  # Kiểm tra thông báo

    def test_booking_missing_fields(self):
        """Kiểm tra đặt sân thất bại do thiếu thông tin"""
        invalid_data = {"scheduleType": "", "date": "", "time": ""}
        response = self.client.post(reverse('booking'), invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vui lòng nhập đầy đủ thông tin")

    def test_booking_redirects_to_payment(self):
        """Kiểm tra đặt sân xong có chuyển sang trang thanh toán không"""
        response = self.client.post(reverse('booking'), self.booking_data)
        self.assertRedirects(response, reverse('payment'))

    def test_duplicate_booking(self):
        """Kiểm tra không thể đặt trùng lịch"""
        Booking.objects.create(schedule_type="fixed", date=date(2025, 2, 10), time=time(14, 0))
        response = self.client.post(reverse('booking'), self.booking_data, follow=True)
        self.assertContains(response, "Lịch đã được đặt trước đó")