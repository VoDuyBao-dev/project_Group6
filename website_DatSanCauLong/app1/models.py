#Quản lý phần đặt lịch
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

def generate_short_id():
    return nanoid.generate(size=5)

class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    # stk = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.user.username

# Court Manager models
class CourtManager(models.Model):
    court_manager_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_manager')

    def __str__(self):
        return self.user.username

# System Admin model
class SystemAdmin(models.Model):
    system_admin_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
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

class Payment(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) # đã thanh toán hay chưa

class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    name = models.CharField(max_length=255, unique=True)
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
    image = models.ImageField(upload_to='app1/static/app1/images', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.day_of_week} | {self.time_frame}"

class Slot(models.Model):
    slot_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='slots') # Gắn với sân
    template = models.ForeignKey(TimeSlotTemplate, on_delete=models.CASCADE, related_name='slots')

# Booking model
class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
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
    payment_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) # đã thanh toán hay chưa

# Court Staff model
class CourtStaff(models.Model):
    court_staff_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    court = models.OneToOneField(Court, on_delete=models.CASCADE, related_name='court_staff')  # Thêm liên kết với một sân

    # def get_court_status(self):
    #     return {c.name: c.slots.all() for c in self.courts.all()}

    # def __str__(self):
    #     return f"{self.user.username} - {self.badminton_hall.name}"

# class CheckIn(models.Model):
#     checkin_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_ins')
#     court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='check_ins')
#     court_staff = models.ForeignKey(CourtStaff, on_delete=models.SET_NULL, null=True, related_name='check_ins')
#     check_in_time = models.DateTimeField(auto_now_add=True)

class Revenue(models.Model):
    revenue_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
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

    # def __str__(self):
    #     return f"Revenue Report ({self.generated_at.date()}) - {self.total_revenue} VND"
