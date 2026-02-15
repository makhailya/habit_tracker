from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для привычки.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity',
            'reward',
            'execution_time',
            'is_public',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Валидация данных на уровне сериализатора.
        """
        # Создаем временный объект для валидации
        habit = Habit(**data)

        # Вызываем метод clean() модели для проверки бизнес-логики
        habit.clean()

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для публичных привычек (только для чтения).
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id',
            'user_email',
            'place',
            'time',
            'action',
            'is_pleasant',
            'periodicity',
            'execution_time',
            'created_at',
        ]
        read_only_fields = fields
        