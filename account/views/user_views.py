from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from account.serializers.user_serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer