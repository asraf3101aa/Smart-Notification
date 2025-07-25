from django.urls import path
from v1.notification.views import NotificationMarkReadAPIView, NotificationListAPIView, NotificationTriggerApiView, UnreadNotificationListAPIView, NotificationChannelPreferenceListCreateAPIView

urlpatterns = [
    path('preferences/', NotificationChannelPreferenceListCreateAPIView.as_view(), name='user_notification_preferences'),
    path('unread/', UnreadNotificationListAPIView.as_view(), name='unread_notifications'),
    path('read/', NotificationMarkReadAPIView.as_view(), name='notification_mark_read'),
    path('history/', NotificationListAPIView.as_view(), name='notification_history'),
    path('trigger/', NotificationTriggerApiView.as_view(), name='notification_trigger'),
]