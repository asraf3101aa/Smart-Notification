from django.urls import  path
from account.views.user_views import CreateUserView, LoginView, UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CreateUserView.as_view(), name="sign_up"),
    path('me/', UserDetailView.as_view(), name='user_detail')
]