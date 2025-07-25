from django.db import models

class NotificationChannel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    IN_APP = 'in_app', 'In App'

class NotificationType(models.TextChoices):
    NEW_COMMENT = 'new_comment', 'New Comment in Subscribed Thread'
    WEEKLY_REPORT = 'weekly_report', 'Weekly Summary Report'
    NEW_DEVICE_LOGIN = 'new_device_login', 'New Device Login Detected'


class NotificationDeliveryStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SENT = 'sent', 'Sent'
    FAILED = 'failed', 'Failed'
    READ = 'read', 'Read'
