from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models.user_models import User
from v1.notification.choices import NotificationChannel, NotificationType
from v1.notification.models import  Notification, NotificationChannelPreference
from thread.models.comment_models import Comment
from v1.notification.tasks import send_preferred_notifications


@receiver(post_save, sender=User)
def create_notification_channel_preference(sender, instance, created, **kwargs):
    if not created:
        return
    
    for notif_type in NotificationType.values:
        for channel in NotificationChannel.values:
            enabled = True
            if channel == NotificationChannel.SMS and not instance.phone_number:
                enabled = False

            NotificationChannelPreference.objects.create(
                user=instance,
                notification_type=notif_type,
                channel=channel,
                enabled=enabled
            )


@receiver(post_save, sender=Comment)
def notify_subscribers(sender, instance, created, **kwargs):
    if not created:
        return

    thread = instance.thread
    subscribers = thread.subscribers.exclude(pk=instance.created_by.pk)

    for subscriber in subscribers:
        preferences = NotificationChannelPreference.objects.filter(
            user=subscriber,
            notification_type=NotificationType.NEW_COMMENT
        )

        if not preferences.exists():
            continue

        # Check if any notification channel is enabled
        if not any(pref.enabled for pref in preferences):
            continue

        notification = Notification.objects.create(
            user = subscriber,
            title=f'New Comment on subscribed thread',
            body=f'{instance.created_by.username} added a new comment on the thread: {thread.title}.',
            notification_type=NotificationType.NEW_COMMENT,
        )

        send_preferred_notifications(notification, subscriber, preferences)
