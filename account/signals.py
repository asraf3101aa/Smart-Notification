from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from account.models.user_models import User, UserLoggedInDevices
from thread.models.thread_models import Thread
from thread.models.comment_models import Comment
from django.contrib.contenttypes.models import ContentType
from v1.notification.choices import  NotificationType
from v1.notification.models import  InAppNotification, Notification, NotificationChannelPreference
from v1.notification.tasks import send_preferred_notifications


@receiver(post_save, sender=User)
def add_user_to_content_creator_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='content creator')
        instance.groups.add(group)


@receiver(post_save, sender=UserLoggedInDevices)
def notify_user_for_new_device(sender, instance, created, **kwargs):
    if not created:
        return
    
    device_count = UserLoggedInDevices.objects.filter(user=instance.user).count()
    if device_count <= 1:
        return
    
    preferences = NotificationChannelPreference.objects.filter(
        user=instance.user,
        notification_type=NotificationType.NEW_COMMENT
    )

    if not any(pref.enabled for pref in preferences):
        return

    notification = Notification.objects.create(
        user = instance.user,
        title=f'Loggedin from new device',
        body=f'You just logged in from device {instance.device_name}.',
        notification_type=NotificationType.NEW_COMMENT,
    )

    send_preferred_notifications(notification, instance.user, preferences)


@receiver(post_save, sender=Group)
def setup_content_creator_group_permissions(sender, instance, created, **kwargs):
    if created and instance.name == 'content creator':
        # Thread permissions
        thread_content_type = ContentType.objects.get_for_model(Thread)
        thread_permissions = Permission.objects.filter(
            content_type=thread_content_type,
            codename__in=[
                'add_thread',
                'change_thread', 
                'delete_thread',
                'view_thread'
            ]
        )
        
        # User permissions (excluding add_user for creation)
        user_content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(
            content_type=user_content_type,
            codename__in=[
                'change_user',
                'delete_user',
                'view_user'
            ]
        )

        # Comment permissions
        comment_content_type = ContentType.objects.get_for_model(Comment)
        comment_permissions = Permission.objects.filter(
            content_type=comment_content_type,
            codename__in=[
                'add_comment',
                'change_comment',
                'delete_comment',
                'view_comment'
            ]
        )

        # Notification preference permissions
        notification_preference_ct = ContentType.objects.get_for_model(NotificationChannelPreference)
        notification_preference_permissions = Permission.objects.filter(
            content_type=notification_preference_ct,
            codename__in=[
                'change_notificationchannelpreference',
                'add_notificationchannelpreference',
                'view_notificationchannelpreference',
            ]
        )

        # In App Notification
        in_app_notification_content_type = ContentType.objects.get_for_model(InAppNotification)
        in_app_notification_permissions = Permission.objects.filter(
            content_type=in_app_notification_content_type,
            codename__in=[
                'change_inappnotification',
            ]
        )

        # Combine all permissions
        all_permissions = list(thread_permissions) + list(user_permissions) + list(comment_permissions) + list(notification_preference_permissions) + list(in_app_notification_permissions)
        if all_permissions:
            instance.permissions.set(all_permissions)