from django.urls import path
from .views import RegisterUserView, ProgressView, PaymentView, LessonListView, LessonDetailView, LoginView, CurrentUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lesson/<int:id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('progress/', ProgressView.as_view(), name='progress'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', CurrentUserView.as_view(), name='current-user'),
]
