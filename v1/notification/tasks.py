from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from account.models.user_models import User
from v1.notification.choices import NotificationChannel, NotificationDeliveryStatus, NotificationType
from v1.notification.models import EmailNotification, InAppNotification, Notification, NotificationChannelPreference, SMSNotification
from thread.models.thread_models import Thread
from datetime import timedelta
from django.utils.timezone import now, make_aware, datetime as dt
from sms import send_sms
import logging
from celery.exceptions import Retry

logger = logging.getLogger(__name__)

def send_preferred_notifications(notification, subscriber, preferences):
    email_pref = preferences.filter(channel=NotificationChannel.EMAIL).first()
    if email_pref and email_pref.enabled:
        send_email_notification.delay(
            notification.id,
            subscriber.email
        )

    in_app_pref = preferences.filter(channel=NotificationChannel.IN_APP).first()
    if in_app_pref and in_app_pref.enabled:
        InAppNotification.objects.create(
            notification=notification,
            status=NotificationDeliveryStatus.SENT
        )

    sms_pref = preferences.filter(channel=NotificationChannel.SMS).first()
    if sms_pref and sms_pref.enabled:
        if subscriber.phone_number:
            send_sms_notification.delay(
                notification.id,
                str(subscriber.phone_number)
            )

@shared_task(bind=True, max_retries=3, default_retry_delay=10) 
def send_email_notification(self, notification_id, subscriber_email):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        logger.warning(f"Notification with id {notification_id} not found.")
        return

    title = notification.title
    content = notification.body
    from_email = settings.DEFAULT_EMAIL_SENDER
    recipient_list = [subscriber_email]

    # Create EmailNotification record
    email_notification = EmailNotification.objects.create(
        notification=notification,
        status=NotificationDeliveryStatus.PENDING,
    )

    try:
        send_mail(
            title,
            content,
            from_email,
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        email_notification.status = NotificationDeliveryStatus.FAILED
        email_notification.error_message = str(e)
        email_notification.save()

        try:
            raise self.retry(exc=e)
        except Retry:
            pass
    else:
        email_notification.status = NotificationDeliveryStatus.SENT
        email_notification.delivered_at = timezone.now()
        email_notification.error_message = None
        email_notification.save()


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_sms_notification(self, notification_id, phone_number):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        logger.warning(f"Notification with id {notification_id} not found.")
        return

    content = notification.body

    # Create SMSNotification record
    sms_notification = SMSNotification.objects.create(
        notification=notification,
        status=NotificationDeliveryStatus.PENDING,
    )

    try:
        send_sms(
            originator=settings.DEFAULT_SMS_SENDER,
            recipients=[phone_number],
            body=content,
        )
    except Exception as e:
        sms_notification.status = NotificationDeliveryStatus.FAILED
        sms_notification.error_message = str(e)
        sms_notification.save()

        try:
            raise self.retry(exc=e)
        except Retry:
            pass 
    else:
        sms_notification.status = NotificationDeliveryStatus.SENT
        sms_notification.delivered_at = timezone.now()
        sms_notification.error_message = None
        sms_notification.save()

@shared_task
def summary_report(report_day=getattr(settings, 'report_day', 0)):
    today = now().date()
    today_weekday = today.weekday()

    days_since_report_day = (today_weekday - report_day) % 7
    end_date = today - timedelta(days=days_since_report_day)
    start_date = end_date - timedelta(days=7)

    start_datetime = make_aware(dt.combine(start_date, dt.min.time()))
    end_datetime = make_aware(dt.combine(end_date, dt.max.time()))

    for user in User.objects.filter(is_active=True, is_superuser=False):
        preferences = NotificationChannelPreference.objects.filter(
            user=user,
            notification_type=NotificationType.WEEKLY_REPORT
        )

        if not any(pref.enabled for pref in preferences):
            continue

        thread_subscription_count = Thread.objects.filter(
            subscribers=user,
            created_at__gte=start_datetime,
            created_at__lte=end_datetime,
        ).count()

        notification = Notification.objects.create(
            user=user,
            title='Weekly Summary',
            body=f'You subscribed to {thread_subscription_count} thread{"s" if thread_subscription_count != 1 else ""} this week.',
            notification_type=NotificationType.WEEKLY_REPORT,
        )

        send_preferred_notifications(notification, user, preferences)