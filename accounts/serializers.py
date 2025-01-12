from rest_framework import serializers
from .models import CustomUser, Lesson
from django.contrib.auth.password_validation import validate_password


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'level', 'video_url', 'file']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(required=True)

    LEVEL_CHOICES = ['beginner', 'intermediate', 'advanced']
    level = serializers.ChoiceField(choices=LEVEL_CHOICES, required=False, default='beginner')

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'level']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            level=validated_data.get('level', 'beginner')
        )
        return user
