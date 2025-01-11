from .models import CustomUser, Progress, Lesson, Payment
from .serializers import UserSerializer, ProgressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LessonSerializer


class LessonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress, created = Progress.objects.get_or_create(user=request.user)
        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        progress, created = Progress.objects.get_or_create(user=request.user)
        completed_lessons = request.data.get('lessons_completed', [])

        for lesson_id in completed_lessons:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                if lesson in request.user.lessons.all():
                    progress.lessons_completed.add(lesson)
                else:
                    return Response(
                        {"error": f"Lesson {lesson_id} is not accessible."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Lesson.DoesNotExist:
                return Response(
                    {"error": f"Lesson {lesson_id} does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            request.user.lessons.add(lesson)
        else:
            payment = Payment.objects.create(
                user=request.user,
                payment_type=payment_type,
                amount=amount
            )
            lessons = Lesson.objects.filter(level=request.user.level)
            request.user.lessons.add(*lessons)

        return Response({
            "message": "Payment successful",
            "payment_id": payment.id,
            "amount": payment.amount
        }, status=status.HTTP_201_CREATED)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome, authenticated user!"})


class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            progress = Progress(user=user)
            progress.save()
            user_serializer = UserSerializer(user)
            progress_serializer = ProgressSerializer(progress)
            return Response({
                'user': user_serializer.data,
                'progress': progress_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
