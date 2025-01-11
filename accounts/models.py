from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Начинающий'), ('intermediate', 'Средний'), ('advanced', 'Продвинутый')],
        default='beginner'
    )
    progress = models.JSONField(default=dict, blank=True)  # Для хранения прогресса
