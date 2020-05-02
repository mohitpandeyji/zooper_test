from django.urls import path

from users.views import UserRegistrationView, UserLoginView, UserDetailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register-user"),
    path('login/', UserLoginView.as_view(), name="login-user"),
    path('users/', UserDetailView.as_view(), name="user-detail-listing")
]
