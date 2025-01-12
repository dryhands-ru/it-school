from .models import CustomUser, Lesson, Payment
from .serializers import UserSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Логин
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Создание токенов
            refresh = RefreshToken.for_user(user)

            # Определяем роль пользователя
            role = 'administrator' if user.is_staff else 'student'

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': role,  # Добавляем роль
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Просмотр уроков
class LessonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        lessons = Lesson.objects.filter(level=user.level)
        completed_lessons = user.lessons_completed.all()

        serialized_lessons = []
        for lesson in lessons:
            accessible = lesson in completed_lessons or (not completed_lessons and lesson == lessons.first())
            serialized_lesson = {
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "level": lesson.level,
                "video_url": lesson.video_url,
                "file": lesson.file.url if lesson.file else None,
                "accessible": accessible,
            }
            serialized_lessons.append(serialized_lesson)

        return Response(serialized_lessons, status=status.HTTP_200_OK)


# Прогресс
class ProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        lessons_completed = user.lessons_completed.all()
        serializer = LessonSerializer(lessons_completed, many=True)
        return Response({
            "user": UserSerializer(user).data,
            "lessons_completed": serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        lesson_id = request.data.get('lesson_id')

        if not lesson_id:
            return Response({"error": "Lesson ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
            if lesson in user.lessons_completed.all():
                return Response({"error": "Lesson already completed."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.lessons_completed.exists() and Lesson.objects.filter(level=user.level).first() == lesson:
                user.lessons_completed.add(lesson)
                return Response({"message": f"Lesson {lesson.title} marked as completed."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Lesson is not accessible."}, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson does not exist."}, status=status.HTTP_404_NOT_FOUND)


# Платежи
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_type = request.data.get('payment_type')
        lesson_id = request.data.get('lesson_id')
        amount = request.data.get('amount')

        if not amount or not payment_type:
            return Response({"error": "Amount and payment_type are required."}, status=status.HTTP_400_BAD_REQUEST)

        if payment_type == 'single' and not lesson_id:
            return Response({"error": "Lesson ID is required for single payments."}, status=status.HTTP_400_BAD_REQUEST)

        if payment_type == 'single':
            try:
                lesson = Lesson.objects.get(id=lesson_id)
            except Lesson.DoesNotExist:
                return Response({"error": "Lesson does not exist."}, status=status.HTTP_404_NOT_FOUND)

            payment = Payment.objects.create(
                user=request.user,
                lesson=lesson,
                payment_type=payment_type,
                amount=amount
            )
            request.user.lessons_completed.add(lesson)
        else:
            payment = Payment.objects.create(
                user=request.user,
                payment_type=payment_type,
                amount=amount
            )
            lessons = Lesson.objects.filter(level=request.user.level)
            request.user.lessons_completed.add(
                *[lesson for lesson in lessons if lesson not in request.user.lessons_completed.all()])

        return Response({
            "message": "Payment successful",
            "payment_id": payment.id,
            "amount": payment.amount,
        }, status=status.HTTP_201_CREATED)


# Регистрация пользователя
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully!',
                'user': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Детали урока
class LessonDetailView(APIView):
    def get(self, request, id):
        try:
            lesson = Lesson.objects.get(id=id)
            serialized_lesson = LessonSerializer(lesson)
            return Response(serialized_lesson.data, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)


# Текущий пользователь
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "role": 'administrator' if request.user.is_staff else 'student',
        })
