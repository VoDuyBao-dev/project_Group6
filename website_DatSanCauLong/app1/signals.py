from django.db.models.signals import post_save
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