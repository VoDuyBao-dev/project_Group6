#Quản lý phần đặt lịch
from django.db import models
from django.contrib.auth.models import User

class Court(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    SCHEDULE_CHOICES = [
        ('fixed', 'Lịch cố định'),
        ('flexible', 'Lịch linh hoạt'),
        ('daily', 'Lịch ngày'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_CHOICES)
    status = models.CharField(max_length=20, default='confirmed')

    def __str__(self):
        return f"{self.user.username} - {self.court.name} - {self.date} {self.time}"