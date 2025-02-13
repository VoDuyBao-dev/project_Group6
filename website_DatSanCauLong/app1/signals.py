from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from app1.models import SystemAdmin, CourtStaff, CourtManager  

# Đảm bảo tất cả nhóm luôn tồn tại trước khi thêm user
def ensure_groups_exist():
    groups = ["Admin", "Court_staff", "Manager", "Customer"]
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

# Đăng ký signal
@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    """Tự động thêm người dùng vào nhóm phù hợp khi được tạo"""
    if created:  # Chỉ chạy khi user vừa được tạo mới
        ensure_groups_exist()  # Đảm bảo tất cả nhóm đã tồn tại

        if instance.is_superuser:  # Nếu là superuser -> nhóm Admin
            admin_group = Group.objects.get(name="Admin")
            instance.groups.add(admin_group)

        elif hasattr(instance, "court_staff"):  # Nếu là CourtStaff -> nhóm CourtStaff
            staff_group = Group.objects.get(name="Court_staff")
            instance.groups.add(staff_group)

        elif hasattr(instance, "court_manager"):  # Nếu là CourtManager -> nhóm CourtManager
            manager_group = Group.objects.get(name="Manager")
            instance.groups.add(manager_group)

        else:  # Mặc định, tất cả user còn lại thuộc nhóm "Customer"
            customer_group = Group.objects.get(name="Customer")
            instance.groups.add(customer_group)
