from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Lesson, Payment

@admin.register(CustomUser)
class CustomUserAdmin(DefaultUserAdmin):
    # Поля, отображаемые в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'role', 'level')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role', 'level', 'is_staff', 'is_superuser', 'is_active')

    # Поля для редактирования пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Стандартные поля
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'level', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'date_of_birth', 'role', 'level'),
        }),
    )

    # Порядок сортировки пользователей
    ordering = ('username',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')  # Указаны только актуальные поля
    search_fields = ('title',)
    list_filter = ('level',)
    ordering = ('title',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_type', 'amount', 'created_at', 'lesson')
    search_fields = ('user__username', 'lesson__title')
    list_filter = ('payment_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
