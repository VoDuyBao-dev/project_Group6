from django.db import models

# Create your models here.

class user(models.Model):
    name = models.CharField(max_length= 50, blank=False)
    email = models.EmailField(max_length= 50, blank=False)
    password = models.CharField(max_length= 50, blank=False)

    def __str__(self):
        return self.name

class test(models.Model):
    name = models.CharField(max_length= 50, blank=False)
   

    def __str__(self):
        return self.name

class Court(models.Model):
    court_id = models.CharField(max_length=100, primary_key=True) 
    badminton_hall_id = models.CharField(max_length=100)  
    location = models.CharField(max_length=255) 
    operating_hours = models.CharField(max_length=255)  
    available_slots = models.JSONField()  

    def update_court_status(self):
        return self.name

class Slot(models.Model):
    slot_id = models.CharField(max_length=100, primary_key=True)  
    time_frame = models.CharField(max_length=100) 
    price_per_frame = models.FloatField()  
    court = models.ForeignKey(Court, on_delete=models.CASCADE)  
    def check_availability(self):
        return self.name

    def book_slot(self):
        return self.name

class Booking(models.Model):
    booking_id = models.CharField(max_length=100, primary_key=True) 
    customer_id = models.CharField(max_length=100) 
    court = models.ForeignKey(Court, on_delete=models.CASCADE)  
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)  
    start_time = models.DateTimeField() 
    end_time = models.DateTimeField()  
    schedule_type = models.CharField(max_length=100)  
    status = models.BooleanField() 

    def booking_action(self, action):
        actions = ["create", "cancel", "modify", "confirm", "payment"]
        if action in actions:
            return f"{action}_booking: {self.booking_id}"
        return "Hành động không hợp lệ"

class Revenue(models.Model):
    revenue_id = models.CharField(max_length=100, primary_key=True)  
    court = models.ForeignKey(Court, on_delete=models.CASCADE) 
    total_revenue = models.FloatField()  
    month = models.IntegerField()  
    quarter = models.IntegerField()  
    year = models.IntegerField()  

    def update_revenue(self):
        return self.name

class Customer(models.Model):
    customer_id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_id


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)


class CourtStaff(models.Model):
    staff_id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id

class CourtManager(models.Model):
    manager_id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.manager_id


class SystemAdmin(models.Model):
    admin_id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin_id


class BadmintonHall(models.Model):
    badminton_hall_id = models.CharField(max_length=50, primary_key=True)
    dia_chi = models.TextField()

    def __str__(self):
        return self.badminton_hall_id


class Court(models.Model):
    court_id = models.CharField(max_length=50, primary_key=True)
    badminton_hall = models.ForeignKey(BadmintonHall, on_delete=models.CASCADE)
    vi_tri = models.TextField()
    gio_hoat_dong = models.CharField(max_length=255)

    def __str__(self):
        return self.court_id


class Slot(models.Model):
    slot_id = models.CharField(max_length=50, primary_key=True)
    khung_gio = models.CharField(max_length=50)
    gia_moi_khung_gio = models.FloatField()
    court = models.ForeignKey(Court, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slot_id} - {self.khung_gio}"


class Booking(models.Model):
    booking_id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    thoi_gian_bat_dau = models.DateTimeField()
    thoi_gian_ket_thuc = models.DateTimeField()
    loai_lich = models.CharField(max_length=50, choices=[('Cố định', 'Cố định'), ('Linh hoạt', 'Linh hoạt'), ('Hàng ngày', 'Hàng ngày')])
    trang_thai = models.BooleanField(default=False)

    def __str__(self):
        return self.booking_id


class Payment(models.Model):
    payment_id = models.CharField(max_length=50, primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tien = models.FloatField()
    trang_thai = models.CharField(max_length=50, choices=[('Chưa thanh toán', 'Chưa thanh toán'), ('Đã thanh toán', 'Đã thanh toán'), ('Hủy', 'Hủy')])

    def __str__(self):
        return self.payment_id


class Revenue(models.Model):
    revenue_id = models.CharField(max_length=50, primary_key=True)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    tong_doanh_thu = models.FloatField(default=0)
    thang = models.IntegerField()
    quy = models.IntegerField()
    nam = models.IntegerField()

    def __str__(self):
        return f"{self.revenue_id} - {self.tong_doanh_thu}"
