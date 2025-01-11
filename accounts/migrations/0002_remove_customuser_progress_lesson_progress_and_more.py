# Generated by Django 5.1.4 on 2025-01-11 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='progress',
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='lessons/')),
                ('teacher', models.CharField(max_length=255)),
                ('students', models.ManyToManyField(related_name='lessons', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lessons_completed', models.ManyToManyField(blank=True, to='accounts.lesson')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='progress_instance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_progress',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.progress'),
        ),
    ]
