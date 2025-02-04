from django.db import models
from django.contrib.auth.models import AbstractUser
import nanoid

# User model
class User(AbstractUser):
    USER_TYPES = (
        ('guest', 'Guest'),
        ('customer', 'Customer'),
        ('court_manager', 'Court Manager'),
        ('court_staff', 'Court Staff'),
        ('admin', 'System Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='guest')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="%(class)s_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="%(class)s_permissions",
        blank=True
    )


class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    # stk = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.user.username

# Court Manager models
class CourtManager(models.Model):
    court_manager_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_manager')

    def __str__(self):
        return self.user.username

# System Admin model
class SystemAdmin(models.Model):
    system_admin_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin')

# Guest model functionality
# class Guest:
# @staticmethod
# def search_courts(criteria):
# return Court.objects.filter(**criteria)

# @staticmethod
# def register_account(username, password, email):
# user = User.register_account(username=username, password=password, email=email, user_type='customer')
# return Customer.objects.create(user=user)


# Booking model
class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    BOOKING_TYPES = (
        ('fixed', 'Fixed'),
        ('daily', 'Daily'),
        ('flexible', 'Flexible'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    court = models.ForeignKey('Court', on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey('Slot', on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    date = models.DateField()
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField(default='00:00:00')
    status = models.BooleanField(default=False) # đã đặt hoặc đã hủy

    def __str__(self):
        return f"Booking for {self.customer.user.username} on {self.date} at {self.start_time}"


class Payment(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) # đã thanh toán hay chưa

class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    system_admin = models.ForeignKey(SystemAdmin, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

# Court model
class Court(models.Model):
    court_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=255)

class TimeSlotTemplate(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )
    template_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    day_of_week = models.CharField(max_length=20) # Thứ (Monday, Tuesday, ...)
    time_frame = models.CharField(max_length=50) # Khung giờ (e.g., 05:00-17:00)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.day_of_week} | {self.time_frame}"

class Slot(models.Model):
    slot_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='slots') # Gắn với sân
    template = models.ForeignKey(TimeSlotTemplate, on_delete=models.CASCADE, related_name='slots')


# Court Staff model
class CourtStaff(models.Model):
    court_staff_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='staff')
    court = models.ManyToManyField(Court, related_name='court_staff', blank=True)  # Thêm liên kết với Court

    def get_court_status(self):
        return {c.name: c.slots.all() for c in self.courts.all()}

    def __str__(self):
        return f"{self.user.username} - {self.badminton_hall.name}"

class CheckIn(models.Model):
    checkin_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_ins')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='check_ins')
    court_staff = models.ForeignKey(CourtStaff, on_delete=models.SET_NULL, null=True, related_name='check_ins')
    check_in_time = models.DateTimeField(auto_now_add=True)

class Revenue(models.Model):
    revenue_id = models.CharField(primary_key=True, max_length=5, default=lambda: nanoid.generate(size=5), editable=False)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='revenue_reports')
    payments = models.ManyToManyField(Payment, related_name='revenues')  # Thêm quan hệ với Payment
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

# from django.db.models import Sum

    # def calculate_total_revenue(self):
    #     """Tính tổng doanh thu dựa trên các khoản thanh toán liên quan"""
    #     total = self.payments.aggregate(total=Sum('amount'))['total']
    #     self.total_revenue = total if total is not None else 0
    #     self.save()

    def __str__(self):
        return f"Revenue Report ({self.generated_at.date()}) - {self.total_revenue} VND"
