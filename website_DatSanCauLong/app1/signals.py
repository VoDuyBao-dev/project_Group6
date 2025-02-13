from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from app1.models import SystemAdmin, CourtStaff, CourtManager  

with open("debug.log", "a") as f:
    f.write(f"instance : \n")
    f.write(f" \n")

# # Đăng ký signal
@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:  # Chỉ chạy khi user vừa được tạo mới
        if instance.is_superuser:  # Nếu là superuser -> nhóm Admin
            group, created = Group.objects.get_or_create(name='Admin')
            instance.groups.add(group)
            SystemAdmin.objects.create(user=instance)  # Thêm người dùng vào model SystemAdmin
            with open("debug.log", "a") as f:
                f.write(f"instance : instance\n")
                f.write(f" \n")

        elif hasattr(instance, CourtStaff):
            group, created = Group.objects.get_or_create(name='Court_staff')
            instance.groups.add(group)
            CourtStaff.objects.create(user=instance)  # Thêm người dùng vào model CourtStaff         

        elif hasattr(instance, CourtManager): 
            group, created = Group.objects.get_or_create(name='Manager')
            instance.groups.add(group)
            CourtManager.objects.create(user=instance)  # Thêm người dùng vào model CourtManager
                
        else:  # Mặc định, tất cả user còn lại thuộc nhóm "Customer"
            group, created = Group.objects.get_or_create(name='Customer')
            instance.groups.add(group)



