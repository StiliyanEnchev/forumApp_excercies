from django.contrib.auth.views import LoginView
from django.urls import path

from djangoTemplates.accounts.views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login')
] 