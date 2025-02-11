from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer, CourtManager

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:  # Kiểm tra nếu User vừa được tạo
        # Chỉ tạo Customer nếu user không phải CourtManager
        if not hasattr(instance, 'court_manager'):
            Customer.objects.create(user=instance)

@receiver(post_save, sender=CourtManager)
def remove_customer_on_court_manager_creation(sender, instance, **kwargs):
    # Nếu user đã tồn tại trong Customer, xóa đối tượng Customer
    if hasattr(instance.user, 'customer'):
        instance.user.customer.delete()

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    # Tự động lưu đối tượng Customer nếu User được cập nhật
    if hasattr(instance, 'customer'):
        instance.customer.save()
