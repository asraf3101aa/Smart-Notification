from rest_framework import serializers
from account.models.user_models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
