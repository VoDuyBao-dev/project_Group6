from django.db import models
from django.contrib.auth.models import AbstractUser
import nanoid

# Hàm tạo ID ngắn gọn
def generate_short_id():
    return nanoid.generate(size=5)

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

    groups = models.ManyToManyField('auth.Group', related_name="%(class)s_groups", blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name="%(class)s_permissions", blank=True)

# Customer model
class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.user.username

# Court Manager model
class CourtManager(models.Model):
    court_manager_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_manager')

    def __str__(self):
        return self.user.username

# System Admin model
class SystemAdmin(models.Model):
    system_admin_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin')

# Badminton Hall model
class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

# Court model
class Court(models.Model):
    STATUS_CHOICES = (
        ('under_maintenance', 'Under Maintenance'),
        ('empty', 'Empty'),
        ('booked', 'Booked'),
    )
    court_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='app1/static/app1/images', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='empty')

    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        return self.image.url if self.image else ''

# TimeSlotTemplate model
class TimeSlotTemplate(models.Model):
    STATUS_CHOICES = (('available', 'Available'), ('unavailable', 'Unavailable'))
    DAY_CHOICES = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ]
    template_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    time_frame = models.CharField(max_length=50)
    time_start = models.TimeField()
    time_end = models.TimeField()
    fixed_price = models.DecimalField(max_digits=6, decimal_places=2)
    daily_price = models.DecimalField(max_digits=6, decimal_places=2)
    flexible_price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.day_of_week} | {self.time_frame}"

# Slot model
class Slot(models.Model):
    slot_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='slots')
    template = models.ForeignKey(TimeSlotTemplate, on_delete=models.CASCADE, related_name='slots')

# Booking model
class Booking(models.Model):
    BOOKING_TYPES = (('fixed', 'Fixed'), ('daily', 'Daily'), ('flexible', 'Flexible'))
    booking_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.booking_id} for {self.customer}"

# Payment model
class Payment(models.Model):
    payment_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

# Revenue model
class Revenue(models.Model):
    revenue_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='revenue_reports')
    payments = models.ManyToManyField(Payment, related_name='revenues')
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
#CourtStaff
class CourtStaff(models.Model):
    court_staff_id = models.CharField(primary_key=True, max_length=5, default=generate_short_id, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    court = models.OneToOneField(Court, on_delete=models.CASCADE, related_name='court_staff')

    def __str__(self):
        return self.user.username