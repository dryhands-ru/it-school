from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]


class CustomUser(AbstractUser):
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner'
    )


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    scheduled_at = models.DateTimeField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    video_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='lessons/', blank=True, null=True)
    teacher = models.CharField(max_length=255)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lessons")

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress_instance"
    )
    lessons_completed = models.ManyToManyField('Lesson', blank=True)

    def __str__(self):
        return f'Progress of {self.user.username}'

    def is_lesson_completed(self, lesson):
        return self.lessons_completed.filter(id=lesson.id).exists()


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('single', 'Поурочно'),
        ('subscription', 'Абонемент'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='payments'
    )
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.payment_type == 'single' and not self.lesson:
            raise ValidationError("Lesson must be provided for single payments.")
        if self.payment_type == 'subscription' and self.lesson:
            raise ValidationError("Lesson should not be provided for subscription payments.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.get_payment_type_display()} - {self.amount}"
