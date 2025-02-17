from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from app1.models import SystemAdmin, CourtStaff, CourtManager, Customer 

# # Đăng ký signal
@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    # with open("debug.log", "a") as f:
    #     f.write(f"instance : {instance}\n")
    #     f.write(f" \n")
    if created:  # Chỉ chạy khi user vừa được tạo mới
        if instance.is_superuser:  # Nếu là superuser -> nhóm Admin
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            instance.groups.add(admin_group)
            SystemAdmin.objects.get_or_create(user=instance)  # Thêm người dùng vào model SystemAdmin

        
# Dùng cho tạo tài khoản ở các giao diện đăng kí và tạo tài khoản.
# Signal xử lý khi CourtManager được tạo
@receiver(post_save, sender=CourtManager)
def handle_court_manager_creation(sender, instance, created, **kwargs):

    if created:
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        instance.user.groups.add(manager_group)

# Signal xử lý khi CourtStaff được tạo
@receiver(post_save, sender=CourtStaff)
def handle_court_staff_creation(sender, instance, created, **kwargs):
    if created:
        staff_group, _ = Group.objects.get_or_create(name='Court_staff')
        instance.user.groups.add(staff_group)


@receiver(post_save, sender=Customer)
def handle_court_customer_creation(sender, instance, created, **kwargs):
    if created:
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        instance.user.groups.add(customer_group)
