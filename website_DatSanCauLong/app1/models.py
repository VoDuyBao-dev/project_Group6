from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import nanoid


class PaymentAccount(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("bank", "Ngân hàng"),
        ("momo", "Momo"),
    ]

    accountHolder = models.CharField(
        max_length=50,
    )
    accountNumber = models.CharField(
        max_length=20,
    )
    paymentMethod = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"{self.accountHolder} - {self.accountNumber}"

def generate_short_id():
    return nanoid.generate(size=5)

        
# Guest and Customer models
class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    # stk = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.user.username

# Court Manager models
class CourtManager(models.Model):
    courtManager_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_manager')
    payment_account = models.OneToOneField(
        PaymentAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='court_manager'
    )
    def __str__(self):
        return self.user.username

# System Admin model
class SystemAdmin(models.Model):
    systemAdmin_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin')


class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


# Court model
class Court(models.Model):
    STATUS_CHOICES = (
        ('under_maintenance', 'Under Maintenance'), # đang bảo trì
        ('empty', 'Empty'),                         # sân trống 
        ('booked', 'Booked'),                       # đã đặt lịch
    )
    court_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='empty')
    def __str__(self):
        return f"{self.name}"
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

class TimeSlotTemplate(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    template_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    time_frame = models.CharField(max_length=50) 
    fixed_price = models.DecimalField(max_digits=6, decimal_places=3)
    daily_price = models.DecimalField(max_digits=6, decimal_places=3)
    flexible_price = models.DecimalField(max_digits=6, decimal_places=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.day_of_week} | {self.time_frame}"


# Booking model
from django.db import models
from django.utils import timezone

class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    
    BOOKING_TYPES = (
        ('fixed', 'Fixed'),
        ('daily', 'Daily'),
        ('flexible', 'Flexible'),
    )
    customer = models.CharField(blank=False, null=False, max_length=5)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    date = models.DateField()
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='00:00:00')
    status = models.BooleanField(default=False) # đã đặt hoặc đã hủy
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_account = models.ForeignKey(
        PaymentAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) # đã thanh toán hay chưa

# Court Staff model
class CourtStaff(models.Model):
    court_staff_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    court = models.OneToOneField(Court, on_delete=models.CASCADE, related_name='court_staff')  # Thêm liên kết với một sân

    # def __str__(self):
    #     return f"{self.user.username} - {self.badminton_hall.name}"

# class CheckIn(models.Model):
#     checkin_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_ins')
#     court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='check_ins')
#     court_staff = models.ForeignKey(CourtStaff, on_delete=models.SET_NULL, null=True, related_name='check_ins')
#     check_in_time = models.DateTimeField(auto_now_add=True)

class RevenueReport(models.Model):
    revenueReport_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='revenue_reports')
    payments = models.ManyToManyField(Payment, related_name='revenues')  # Thêm quan hệ với Payment
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)





