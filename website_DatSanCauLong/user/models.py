





# Bài của mình vẫn chưa xong nha tại buồn ngủ nên chỉ được chừng này thui.

# Bài chưa kịp xong nha.
# Sắp 12h òi mẹ bắt đi ngủ òi nha.




from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

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
        related_name='user_user_set',  # Add related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_user_set',  # Add related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Guest and Customer models
class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
    return self.user.username

# System Admin model
class SystemAdmin(models.Model):
    systemadmin_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin')

    def __str__(self):
    return self.user.username


# Court Staff model
class CourtStaff(models.Model):
    courtstaff_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    branch = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return self.user.username

# Booking model
class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    BOOKING_TYPES = (
        ('fixed', 'Fixed'),
        ('daily', 'Daily'),
        ('flexible', 'Flexible'),
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    court_id = models.ForeignKey('Court', on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE) 
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.FloatField(null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.customer_id} on {self.date} at {self.start_time}"

class Slot(models.Model):
    slot_id = models.CharField(max_length=100, primary_key=True)  
    time_frame = models.CharField(max_length=100) 
    price_per_frame = models.FloatField()  
    court = models.ForeignKey(Court, on_delete=models.CASCADE)  

class Payment(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')))

# Court Branch model
class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    systemadmin_id = models.ForeignKey(SystemAdmin, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

# Court model
class Court(models.Model):
    court_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    badminton_hall_id = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=255)
    hourly_rate_fixed = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate_daily = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate_flexible = models.DecimalField(max_digits=10, decimal_places=2)
    time_slots = models.JSONField(default=dict)  # Example with rates

    def check_availability(self, time_slot):
        return self.time_slots.get(time_slot, {}).get("status") == "available"

# Example predefined time slots with pricing
# DEFAULT_TIME_SLOTS = {
#     "Monday": {
#         "05:00-17:00": {"fixed": 60, "daily": 70, "flexible": 60, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 60, "daily": 60, "flexible": 60, "status": "available"},
#     },
#     "Tuesday": {
#         "05:00-17:00": {"fixed": 60, "daily": 70, "flexible": 60, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 60, "daily": 60, "flexible": 60, "status": "available"},
#     },
#     "Wednesday": {
#         "05:00-17:00": {"fixed": 60, "daily": 70, "flexible": 60, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 60, "daily": 60, "flexible": 60, "status": "available"},
#     },
#     "Thursday": {
#         "05:00-17:00": {"fixed": 60, "daily": 70, "flexible": 60, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 60, "daily": 60, "flexible": 60, "status": "available"},
#     },
#     "Friday": {
#         "05:00-17:00": {"fixed": 60, "daily": 70, "flexible": 60, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 60, "daily": 60, "flexible": 60, "status": "available"},
#     },
#     "Saturday": {
#         "05:00-17:00": {"fixed": 90, "daily": 100, "flexible": 90, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 60, "daily": 60, "flexible": 60, "status": "available"},
#     },
#     "Sunday": {
#         "05:00-17:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "17:00-22:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#         "22:00-24:00": {"fixed": 100, "daily": 120, "flexible": 100, "status": "available"},
#     },
# }

# CheckIn model
class CheckIn(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_ins')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='check_ins')
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check-in for {self.booking}"

# Revenue Report model
class Revenue(models.Model):
    revenue_id = models.CharField(max_length=100, primary_key=True)  
    court = models.ForeignKey(Court, on_delete=models.CASCADE) 
    total_revenue = models.FloatField()  
    month = models.FloatField()  
    quarter = models.FloatField()  
    year = models.FloatField()  
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def update_revenue(self):
        return self.name
