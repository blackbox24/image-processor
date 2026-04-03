from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="account_login"),
    path("signup", views.SignUpView.as_view(), name="account_signup"),
]
