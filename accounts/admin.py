from django.contrib import admin
from .models import CustomUser, Lesson, Progress


admin.site.register(CustomUser)
admin.site.register(Lesson)
admin.site.register(Progress)