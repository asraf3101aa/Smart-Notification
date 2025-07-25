from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from account.models.user_models import User, UserLoggedInDevices

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = BaseUserAdmin.list_display + ('phone_number',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

@admin.register(UserLoggedInDevices)
class UserLoggedInDevicesAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_token', 'device_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'device_token', 'device_name')
    list_filter = ('created_at',)



