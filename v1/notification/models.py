from django.db import models
from django.contrib.auth import get_user_model
from v1.notification.choices import NotificationChannel, NotificationDeliveryStatus, NotificationType

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)

    def __str__(self):
        return self.title

class BaseChannelNotification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=NotificationDeliveryStatus.choices,
        default=NotificationDeliveryStatus.PENDING
    )
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract = True


class InAppNotification(BaseChannelNotification):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='in_app_notifications')


class EmailNotification(BaseChannelNotification):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='email_notifications')
    delivered_at = models.DateTimeField(blank=True, null=True)


class SMSNotification(BaseChannelNotification):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='sms_notifications')
    delivered_at = models.DateTimeField(blank=True, null=True)


class NotificationChannelPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    channel = models.CharField(max_length=10, choices=NotificationChannel.choices)
    enabled = models.BooleanField()

    class Meta:
        unique_together = ('user', 'notification_type', 'channel')