from django.urls import path

from .views import (UserDetailView, UserLoginView, UserLogoutView,
                    UserRegisterView)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("detail/", UserDetailView.as_view(), name="user_detail"),
]
