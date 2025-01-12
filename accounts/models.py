from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Уровни обучения
LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

# Роли пользователей
ROLE_CHOICES = [
    ('student', 'Student'),
    ('administrator', 'Administrator'),
]

class CustomUser(AbstractUser):
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner',
        verbose_name="Уровень обучения"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name="Роль пользователя"
    )
    lessons_completed = models.ManyToManyField('Lesson', blank=True, verbose_name="Пройденные уроки")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.username

    def get_dashboard_url(self):
        """Возвращает URL для личного кабинета на основе роли."""
        if self.role == 'administrator':
            return '/administrator/dashboard'
        return '/dashboard'

class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, verbose_name="Уровень")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    file = models.FileField(upload_to='lessons/', blank=True, null=True, verbose_name="Файл")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('single', 'Поурочно'),
        ('subscription', 'Абонемент'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='payments',
        verbose_name="Занятие"
    )
    payment_type = models.CharField(
        max_length=15,
        choices=PAYMENT_TYPE_CHOICES,
        verbose_name="Тип оплаты"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

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
