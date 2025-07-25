from rest_framework.generics import CreateAPIView,  RetrieveUpdateDestroyAPIView
from account.serializers.user_serializers import CustomTokenObtainPairSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class LoginView(TokenObtainPairView):
    """
    API view to obtain JWT token pair for user login.
    Accessible to anyone (no authentication required).
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class CreateUserView(CreateAPIView):
    """
    API view to register a new user. Accessible to anyone (no authentication required).
    """
    permission_classes=[AllowAny ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete the profile of the requesting user.
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user