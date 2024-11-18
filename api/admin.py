from django.contrib import admin
from django.contrib.auth import get_user_model
from . import models

# Register your models here.

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'user_role']
    list_display = ['username', 'email', 'phone_no', 'user_role']
    class Meta:
        model = User


class LeavesAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['user', 'leave_reason', 'start_leave_date', 'end_leave_date', 'applied_leave_date', 'leave_status']
    class Meta:
        model = models.LeaveModel

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'leave']
    class Meta:
        model = models.ProfileModel

admin.site.register(User, UserAdmin)
admin.site.register(models.LeaveModel, LeavesAdmin)
admin.site.register(models.ProfileModel, ProfileAdmin)

