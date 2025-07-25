from django.contrib import admin
from v1.notification.models import EmailNotification, InAppNotification, NotificationChannelPreference, SMSNotification

@admin.register(NotificationChannelPreference)
class NotificationChannelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'channel', 'enabled')
    list_filter = ('notification_type', 'channel', 'enabled')
    search_fields = ('user__username', 'user__email')

class BaseChannelNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification', 'get_receiver', 'status', 'created_at', 'error_message')
    list_filter = ('status', 'created_at')
    search_fields = ('notification__title', 'error_message', 'notification__user__email')
    readonly_fields = ('created_at',)

    def get_receiver(self, obj):
        return obj.notification.user
    get_receiver.short_description = 'Receiver'

@admin.register(InAppNotification)
class InAppNotificationAdmin(BaseChannelNotificationAdmin):
    pass

@admin.register(EmailNotification)
class EmailNotificationAdmin(BaseChannelNotificationAdmin):
    list_display = BaseChannelNotificationAdmin.list_display + ('delivered_at',)
    readonly_fields = BaseChannelNotificationAdmin.readonly_fields + ('delivered_at',)

@admin.register(SMSNotification)
class SMSNotificationAdmin(BaseChannelNotificationAdmin):
    list_display = BaseChannelNotificationAdmin.list_display + ('delivered_at',)
    readonly_fields = BaseChannelNotificationAdmin.readonly_fields + ('delivered_at',)