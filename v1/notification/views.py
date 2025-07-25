from django.db import IntegrityError, transaction
from django.forms import ValidationError
from thread.models.thread_models import Thread
from v1.notification.choices import NotificationDeliveryStatus
from v1.notification.tasks import summary_report
from .models import InAppNotification, NotificationChannelPreference
from .serializers import InAppNotificationSerializer, NotificationMarkReadSerializer, NotificationSerializer, NotificationChannelPreferenceSerializer
from rest_framework.generics import  ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from thread.models.comment_models import Comment
from datetime import datetime

class NotificationChannelPreferenceListCreateAPIView(ListCreateAPIView):
    """
    API view to list and create notification channel preferences 
    for the requesting user.
    """
    permission_classes = [DjangoModelPermissions]
    serializer_class = NotificationChannelPreferenceSerializer

    def get_queryset(self):
        return NotificationChannelPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnreadNotificationListAPIView(ListAPIView):
    """
    API view to list all unread notifications for the requesting user.
    """
    serializer_class = InAppNotificationSerializer

    def get_queryset(self):
        return InAppNotification.objects.filter(notification__user=self.request.user, status=NotificationDeliveryStatus.SENT)
    

class NotificationMarkReadAPIView(APIView):
    """
    API view to mark one or more unread notifications as read 
    for the currently authenticated user. Expects a list of notification IDs in the request body.
    """
    serializer_class = NotificationMarkReadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification_ids = serializer.validated_data['ids']
        user = request.user

        # Filter notifications belonging to this user and unread
        notifications = InAppNotification.objects.filter(
            notification__user=user,
            id__in=notification_ids,
            status=NotificationDeliveryStatus.SENT
        )

        if not notifications.exists():
            return Response({"detail": "No unread notifications found for given IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_count = notifications.update(status=NotificationDeliveryStatus.READ)

        return Response({"detail": f"{updated_count} notification(s) marked as read."},
                        status=status.HTTP_200_OK)


class NotificationListAPIView(ListAPIView):
    """
    API view to list all notifications for the currently authenticated user,
    regardless of read/unread status.
    """
    serializer_class = InAppNotificationSerializer

    def get_queryset(self):
        return InAppNotification.objects.filter(notification__user=self.request.user)
    

class NotificationTriggerApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Trigger the summary report for the current day of the week.
        """
        try:
            today_weekday = datetime.today().weekday()  # 0 = Monday, 6 = Sunday
            summary_report.delay(report_day=today_weekday)

            return Response(
                {"detail": "Weekly summary report triggered successfully."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Failed to trigger summary report.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )