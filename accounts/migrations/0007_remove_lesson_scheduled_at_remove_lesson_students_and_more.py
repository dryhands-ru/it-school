# Generated by Django 5.1.4 on 2025-01-12 18:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_lesson_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='scheduled_at',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='students',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('administrator', 'Administrator')], default='student', max_length=20, verbose_name='Роль пользователя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='lessons_completed',
            field=models.ManyToManyField(blank=True, to='accounts.lesson', verbose_name='Пройденные уроки'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20, verbose_name='Уровень обучения'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(verbose_name='Описание урока'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='lessons/', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название урока'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accounts.lesson', verbose_name='Занятие'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('single', 'Поурочно'), ('subscription', 'Абонемент')], max_length=15, verbose_name='Тип оплаты'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
