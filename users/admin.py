from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Админка для кастомной модели пользователя.
    """
    list_display = ['email', 'username', 'telegram_chat_id', 'is_staff']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email', 'username', 'telegram_chat_id']

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('telegram_chat_id',)}),
    )
