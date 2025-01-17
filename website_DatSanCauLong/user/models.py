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
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    @staticmethod
    def register_account(username, password, email, user_type='customer'):
        if user_type not in dict(User.USER_TYPES):
            raise ValueError("Invalid user type.")
        user = User.objects.create_user(username=username, password=password, email=email, user_type=user_type)
        return user

    def login(self, username, password):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                raise ValueError("Incorrect password.")
        except User.DoesNotExist:
            raise ValueError("User does not exist.")

# Guest and Customer models
class Customer(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def book_court(self, court, booking_type, date, start_time, end_time, total_hours=None):
        booking = Booking.objects.create(
            customer=self, court=court, booking_type=booking_type, date=date,
            start_time=start_time, end_time=end_time, total_hours=total_hours
        )
        if not court.branch.manager:
            raise ValueError("Court branch has no manager assigned.")
        booking.payment_status = False  # Customer bookings require payment verification
        booking.save()
        return booking

    def check_in(self, court):
        return CheckIn.objects.create(customer=self, court=court)

    def login(self, username, password):
        return self.user.login(username, password)

# Guest model functionality
class Guest:
    @staticmethod
    def search_courts(criteria):
        return Court.objects.filter(**criteria)

    @staticmethod
    def register_account(username, password, email):
        user = User.register_account(username=username, password=password, email=email, user_type='customer')
        return Customer.objects.create(user=user)



class Payment(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')))

    @staticmethod
    def process_payment(booking, amount):
        payment = Payment.objects.create(booking=booking, amount=amount, status='completed')
        booking.payment_status = True
        booking.save()
        return payment

    @staticmethod
    def auto_process_payment(booking):
        if not booking.payment_status:
            amount = booking.calculate_cost()
            Payment.objects.create(booking=booking, amount=amount, status='completed')
            booking.payment_status = True
            booking.save()

# Court Manager models
class CourtManager(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_manager')

    def register_court(self, branch, name, hourly_rate_fixed, hourly_rate_daily, hourly_rate_flexible, time_slots):
        return Court.objects.create(
            branch=branch, name=name, hourly_rate_fixed=hourly_rate_fixed,
            hourly_rate_daily=hourly_rate_daily, hourly_rate_flexible=hourly_rate_flexible,
            time_slots=time_slots
        )

    def manage_courts(self):
        return Court.objects.filter(branch__manager=self)

    def book_court_for_customer(self, customer, court, booking_type, date, start_time, end_time, total_hours):
        booking = Booking.objects.create(
            customer=customer, court=court, booking_type=booking_type, date=date,
            start_time=start_time, end_time=end_time, total_hours=total_hours,
            payment_status=True  # Automatically mark as paid for manager-initiated bookings
        )
        Payment.auto_process_payment(booking)
        return booking

    def login(self, username, password):
        return self.user.login(username, password)

# Court Branch model
class CourtBranch(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    manager = models.ForeignKey(CourtManager, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField()

    def add_court(self, name, hourly_rate_fixed, hourly_rate_daily, hourly_rate_flexible, time_slots):
        return Court.objects.create(
            branch=self, name=name, hourly_rate_fixed=hourly_rate_fixed,
            hourly_rate_daily=hourly_rate_daily, hourly_rate_flexible=hourly_rate_flexible,
            time_slots=time_slots
        )


# Court Staff model
class CourtStaff(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='court_staff')
    branch = models.ForeignKey(CourtBranch, on_delete=models.CASCADE, related_name='staff')

    def check_in_customer(self, customer, court):
        return CheckIn.objects.create(customer=customer, court=court)

    def monitor_courts(self):
        return Court.objects.filter(branch=self.branch)

    def login(self, username, password):
        return self.user.login(username, password)

# CheckIn model
class CheckIn(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='check_ins')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='check_ins')
    check_in_time = models.DateTimeField(auto_now_add=True)

    def record_check_in(self):
        self.save()

# System Admin model
class SystemAdmin(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin')

    def manage_users(self):
        return User.objects.all()

    def manage_branches(self):
        return CourtBranch.objects.all()

    def register_branch(self, name, address, manager):
        return CourtBranch.objects.create(name=name, address=address, manager=manager)

    def register_account(self, username, password, email, user_type):
        if user_type not in ['court_manager', 'court_staff']:
            raise ValueError("Invalid user type for this method.")
        user = User.objects.create_user(username=username, password=password, email=email, user_type=user_type)
        if user_type == 'court_manager':
            return CourtManager.objects.create(user=user)
        elif user_type == 'court_staff':
            return CourtStaff.objects.create(user=user)

    def login(self, username, password):
        return self.user.login(username, password)

    def view_system_revenue(self, start_date, end_date):
        report = RevenueReport(start_date=start_date, end_date=end_date)
        report.generate_report()
        return report

