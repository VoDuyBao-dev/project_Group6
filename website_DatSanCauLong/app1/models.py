from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid

# User model
# class User(AbstractUser):
#     USER_TYPES = (
#     ('guest', 'Guest'),
#     ('customer', 'Customer'),
#     ('court_manager', 'Court Manager'),
#     ('court_staff', 'Court Staff'),
#     ('admin', 'System Admin'),
#     )
#     user_type = models.CharField(max_length=20, choices=USER_TYPES, default='guest')

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='user_user_set', # Add related_name to avoid clashes
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         verbose_name='groups',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='user_user_set', # Add related_name to avoid clashes
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

# Guest and Customer models
class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    Thongtintaikhoan = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    # stk = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.user.username

# Court Manager models
class CourtManager(models.Model):
    courtManager_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    Thongtintaikhoan = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_manager')

    def __str__(self):
        return self.user.username

# System Admin model
class SystemAdmin(models.Model):
    systemAdmin_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    Thongtintaikhoan = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin')


class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

# Court model
class Court(models.Model):
    court_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    badminton_hall_id = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, default='c1', related_name='courts')
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
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
    template_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    day_of_week = models.CharField(max_length=20) # Thứ (Monday, Tuesday, ...)
    time_frame = models.CharField(max_length=50) # Khung giờ (e.g., 05:00-17:00)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.day_of_week} | {self.time_frame}"

class Slot(models.Model):
    slot_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    court_id = models.ForeignKey('Court', on_delete=models.CASCADE, related_name='slots') # Gắn với sân
    template_id = models.ForeignKey(TimeSlotTemplate, on_delete=models.CASCADE, default='s1', related_name='slots')

# Booking model
class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    BOOKING_TYPES = (
    ('fixed', 'Fixed'),
    ('daily', 'Daily'),
    ('flexible', 'Flexible'),
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    court_id = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='bookings')
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    date = models.DateField()
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='00:00:00')
    status = models.BooleanField(default=False) # đã đặt hoặc đã hủy

    def __str__(self):
        return f"Booking for {self.customer} on {self.date} at {self.time}"

class Payment(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE, default='p1', related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) # đã thanh toán hay chưa

# Court Staff model
class CourtStaff(models.Model):
    courtStaff_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    Thongtintaikhoan = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    badminton_hall_id = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, default='cs1', related_name='staff')

# # CheckIn model
# class CheckIn(models.Model):
# id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
# customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_ins')
# court_idid = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='check_ins')
# check_in_time = models.DateTimeField(auto_now_add=True)

# Revenue Report model
class RevenueReport(models.Model):
    revenueReport_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    badminton_hall_id = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='revenue_reports',
    null=True, blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)