from django.urls import path
from .views import UserListView, RegisterUserView, ProtectedView, ProgressView, PaymentView, LessonListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('progress/', ProgressView.as_view(), name='progress'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('payment/', PaymentView.as_view(), name='payment'),
]
