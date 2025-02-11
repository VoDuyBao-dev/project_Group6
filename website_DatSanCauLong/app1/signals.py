from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer, CourtManager, SystemAdmin, CourtStaff

# Signal quản lý User
@receiver(post_save, sender=User)
# def manage_user_roles(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_superuser:
#             # Thêm vào bảng SystemAdmin nếu là admin
#             SystemAdmin.objects.get_or_create(user=instance)
#         else:
#             # Nếu không phải admin, tạo Customer (tạm thời)
#             Customer.objects.get_or_create(user=instance)

#     else:
#         if instance.is_superuser:
#             # Nếu là admin, thêm vào bảng SystemAdmin
#             SystemAdmin.objects.get_or_create(user=instance)
#             # Xóa Customer nếu tồn tại
#             Customer.objects.filter(user=instance).delete()
#         else:
#             # Nếu không phải admin, đảm bảo vẫn là Customer
#             Customer.objects.get_or_create(user=instance)
def manage_user_roles(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            SystemAdmin.objects.get_or_create(user=instance)
        else:
            # Chỉ tạo Customer nếu user không thuộc CourtManager hoặc CourtStaff
            if not hasattr(instance, 'court_manager') and not hasattr(instance, 'court_staff'):
                Customer.objects.get_or_create(user=instance)
    else:
        if instance.is_superuser:
            SystemAdmin.objects.get_or_create(user=instance)
            Customer.objects.filter(user=instance).delete()
        else:
            # Kiểm tra lại để xóa Customer nếu user được cập nhật làm Manager/Staff
            if hasattr(instance, 'court_manager') or hasattr(instance, 'court_staff'):
                Customer.objects.filter(user=instance).delete()
            else:
                Customer.objects.get_or_create(user=instance)
    
# Signal xử lý khi CourtManager được tạo
@receiver(post_save, sender=CourtManager)
def handle_court_manager_creation(sender, instance, created, **kwargs):

    if created:
        Customer.objects.filter(user=instance.user).delete()

# Signal xử lý khi CourtStaff được tạo
@receiver(post_save, sender=CourtStaff)
def handle_court_staff_creation(sender, instance, created, **kwargs):
    if created:
        Customer.objects.filter(user=instance.user).delete()
