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

    def create_booking(self):
        return self.name

    def cancel_booking(self):
        return self.name

    def modify_booking(self):
        return self.name
    def confirm_booking(self):
        return self.name

    def confirm_payment(self):
        return self.name

class Revenue(models.Model):
    revenue_id = models.CharField(max_length=100, primary_key=True)  
    court = models.ForeignKey(Court, on_delete=models.CASCADE) 
    total_revenue = models.FloatField()  
    month = models.FloatField()  
    quarter = models.FloatField()  
    year = models.FloatField()  

    def update_revenue(self):
        return self.name

       