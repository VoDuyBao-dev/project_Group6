from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(CourtManager)
admin.site.register(SystemAdmin)
admin.site.register(BadmintonHall)
admin.site.register(Court)
admin.site.register(TimeSlotTemplate)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(CourtStaff)
admin.site.register(RevenueReport)



