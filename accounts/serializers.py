from .models import CustomUser
from rest_framework import serializers
from .models import Progress, Lesson
from django.contrib.auth import get_user_model


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'level', 'video_url', 'file']


class ProgressSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Показываем имя пользователя
    lessons_completed = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Progress
        fields = ['user', 'lessons_completed']


class UserSerializer(serializers.ModelSerializer):
    # Здесь будет сериализатор для поля progress
    progress = ProgressSerializer(read_only=True)  # Используем сериализатор Progress для поля progress

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'level', 'progress']
