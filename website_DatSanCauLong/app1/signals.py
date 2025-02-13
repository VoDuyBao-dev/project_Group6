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

from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from app1.models import SystemAdmin, CourtStaff, CourtManager  

@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    """Tự động thêm người dùng vào nhóm phù hợp khi được tạo"""
    if created:  # Chỉ chạy khi user vừa được tạo mới
        if instance.is_superuser:  # Nếu là superuser -> nhóm Admin
            admin_group, _ = Group.objects.get_or_create(name="Admin")
            instance.groups.add(admin_group)

        elif hasattr(instance, "court_staff"):  # Nếu là CourtStaff -> nhóm CourtStaff
            staff_group, _ = Group.objects.get_or_create(name="Court_staff")
            instance.groups.add(staff_group)

        elif hasattr(instance, "court_manager"):  # Nếu là CourtManager -> nhóm CourtManager
            manager_group, _ = Group.objects.get_or_create(name="Manager")
            instance.groups.add(manager_group)

