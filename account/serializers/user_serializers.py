from rest_framework import serializers
from account.models.user_models import User, UserLoggedInDevices
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ['id','email', 'username','first_name', 'last_name', 'password','phone_number']

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate_phone_number(self, value):
        user = self.instance
        if User.objects.filter(phone_number=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError("This phone_number is already in use.")
        return value
    
    def validate_username(self, value):
        user = self.instance
        if User.objects.filter(username=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        required_fields = ['email', 'username', 'password']
        missing_fields = [field for field in required_fields if field not in validated_data]

        if missing_fields:
            raise serializers.ValidationError({
                field: ["This field is required."] for field in missing_fields
            })

        return User.objects.create_user(**validated_data)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    device_id = serializers.CharField(write_only=True)
    device_name = serializers.CharField(write_only=True) 

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        device_id = attrs.get('device_id')
        device_name = attrs.get('device_name')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid username or password')

        if user.is_deleted:
            raise serializers.ValidationError('User account is deleted')

        UserLoggedInDevices.objects.get_or_create(
            user=user,
            device_token=device_id,
            defaults={'device_name': device_name}
        )

        data = super().validate(attrs)

        return data
