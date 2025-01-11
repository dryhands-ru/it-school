from django.urls import path
from .views import UserListView, RegisterUserView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegisterUserView.as_view(), name='register'),
]
