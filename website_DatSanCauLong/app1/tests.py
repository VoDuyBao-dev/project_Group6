import uuid
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from app1.models import Booking, Court, Customer
from datetime import timedelta

class BookingTestCase(TestCase):
    def setUp(self):
        # Tạo user và customer
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.customer = Customer.objects.create(user=self.user)

        # Tạo sân
        self.court = Court.objects.create(name="Court 1", status="available")

    def test_booking_valid(self):
        """ Kiểm tra đặt sân hợp lệ (đặt trước đúng 1 năm) """
        booking_date = timezone.now().date() + timedelta(days=365)  # Đặt trước đúng 1 năm
        booking = Booking.objects.create(
            id=uuid.uuid4(),  # Tạo UUID hợp lệ
            customer=self.customer,
            court=self.court,
            date=booking_date,
            start_time="14:00",
            end_time="16:00"
        )
        self.assertIsNotNone(booking.id)

    def test_booking_exceeds_one_year(self):
        """ Không cho phép đặt sân quá 1 năm """
        booking_date = timezone.now().date() + timedelta(days=366)
        with self.assertRaises(Exception):
            Booking.objects.create(
                id=uuid.uuid4(),
                customer=self.customer,
                court=self.court,
                date=booking_date,
                start_time="10:00",
                end_time="12:00"
            )

    def test_booking_in_the_past(self):
        """ Không cho phép đặt ngày trong quá khứ """
        booking_date = timezone.now().date() - timedelta(days=1)
        with self.assertRaises(Exception):
            Booking.objects.create(
                id=uuid.uuid4(),
                customer=self.customer,
                court=self.court,
                date=booking_date,
                start_time="08:00",
                end_time="10:00"
            )

    def test_booking_without_customer(self):
        """ Kiểm tra không thể đặt sân nếu khách hàng không tồn tại """
        with self.assertRaises(Exception):
            Booking.objects.create(
                id=uuid.uuid4(),
                customer=None,
                court=self.court,
                date=timezone.now().date(),
                start_time="12:00",
                end_time="14:00"
            )

    def test_booking_invalid_time(self):
        """ Kiểm tra đặt sân với giờ không hợp lệ (giờ bắt đầu sau giờ kết thúc) """
        with self.assertRaises(Exception):
            Booking.objects.create(
                id=uuid.uuid4(),
                customer=self.customer,
                court=self.court,
                date=timezone.now().date() + timedelta(days=2),
                start_time="18:00",
                end_time="16:00"  # Giờ kết thúc nhỏ hơn giờ bắt đầu
            )
