from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, confirm_email

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),
]
