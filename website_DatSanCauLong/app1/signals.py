from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from app1.models import Customer
from app1.utils import generate_short_id  # Nhớ kiểm tra utils.py đã có hàm này

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:  # Nếu user mới được tạo
        Customer.objects.create(
            user=instance,
            customer_id=generate_short_id()  # Tạo ID tự động
        )
