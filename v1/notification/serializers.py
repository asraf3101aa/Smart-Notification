from rest_framework import serializers
from v1.notification.choices import NotificationChannel
from v1.notification.models import BaseChannelNotification, InAppNotification, Notification, NotificationChannelPreference


class NotificationChannelPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannelPreference
        fields = ['notification_type', 'channel', 'enabled']

    def validate_enabled(self, value):
        """
        Prevent enabling SMS if user has no phone number.
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        channel = self.initial_data.get('channel')

        if channel == NotificationChannel.SMS and value and not getattr(user, 'phone_number', None):
            raise serializers.ValidationError("Cannot enable SMS notifications without a phone number.")
        return value
    
    def create(self, validated_data):
        user = validated_data['user']
        notification_type = validated_data['notification_type']
        channel = validated_data['channel']
        enabled = validated_data['enabled']

        instance, _ = NotificationChannelPreference.objects.update_or_create(
            user=user,
            notification_type=notification_type,
            channel=channel,
            defaults={'enabled': enabled}
        )
        return instance


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'notification_type']

    def create(self, validated_data):
        user = validated_data['user']
        notification_type = validated_data['notification_type']
        channel = validated_data['channel']
        enabled = validated_data['enabled']

        instance, _ = NotificationChannelPreference.objects.update_or_create(
            user=user,
            notification_type=notification_type,
            channel=channel,
            defaults={'enabled': enabled}
        )
        return instance
    
    
class BaseChannelNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = BaseChannelNotification
        fields = ['created_at', 'status', 'error_message']
        abstract = True


class InAppNotificationSerializer(BaseChannelNotificationSerializer):
    class Meta:
        model = InAppNotification
        fields = BaseChannelNotificationSerializer.Meta.fields + ['notification']


class NotificationMarkReadSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        write_only=True,
    )