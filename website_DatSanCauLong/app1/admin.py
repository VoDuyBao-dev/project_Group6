from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.

    

# Hàm tự động gán nhóm
def add_user_to_group(user, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)

# Tùy chỉnh hiển thị SystemAdmin
@admin.register(SystemAdmin)
class SystemAdminAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)

# Khi SystemAdmin tạo CourtStaff, tự động gán vào nhóm CourtStaff
@admin.register(CourtStaff)
class CourtStaffAdmin(admin.ModelAdmin):
    list_display = ("user", "court_staff_id")                          # Tên cột hiển thị trên trang admin
    search_fields = ("user__username", "court_staff_id")   # Tìm kiếm theo tên và id

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        add_user_to_group(obj.user, "Court_staff")  # Thêm vào nhóm Court_staff

# Khi SystemAdmin tạo CourtManager, tự động gán vào nhóm CourtManager
from django.contrib import admin
from .models import CourtManager, BadmintonHall

@admin.register(CourtManager)
class CourtManagerAdmin(admin.ModelAdmin):
    list_display = ("user", "get_badminton_hall")  # Hiển thị tên + chi nhánh
    search_fields = ("user__username",)

    def get_badminton_hall(self, obj):
        # Lấy chi nhánh từ badminton_hall (quan hệ ngược)
        if hasattr(obj, 'badminton_hall'):
            return obj.badminton_hall.name
        return "Chưa có chi nhánh"
    
    get_badminton_hall.short_description = "Chi Nhánh"


# các model còn lại
admin.site.register(Customer)
admin.site.register(BadmintonHall)
admin.site.register(Court)
admin.site.register(TimeSlotTemplate)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(RevenueReport)
admin.site.register(PaymentAccount)



