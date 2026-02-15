from django.db import models
from django.conf import settings
from .validators import (
    validate_execution_time,
    validate_periodicity,
    validate_pleasant_habit,
    validate_reward_and_related_habit,
    validate_related_habit_is_pleasant
)


class Habit(models.Model):
    """
    Модель привычки.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место',
        help_text='Место, в котором необходимо выполнять привычку'
    )
    time = models.TimeField(
        verbose_name='Время',
        help_text='Время, когда необходимо выполнять привычку'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие',
        help_text='Действие, которое представляет собой привычка'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Является ли привычка приятной'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_habits',
        verbose_name='Связанная привычка',
        help_text='Привычка, которая связана с другой привычкой'
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[validate_periodicity],
        verbose_name='Периодичность',
        help_text='Периодичность выполнения привычки в днях (от 1 до 7)'
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение',
        help_text='Чем пользователь должен себя вознаградить после выполнения'
    )
    execution_time = models.PositiveIntegerField(
        validators=[validate_execution_time],
        verbose_name='Время на выполнение',
        help_text='Время, которое потребуется на выполнение привычки в секундах'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности',
        help_text='Можно ли публиковать привычку в общий доступ'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    def clean(self):
        """
        Валидация модели на уровне объекта.
        """
        super().clean()

        # Проверка приятной привычки
        validate_pleasant_habit(self)

        # Проверка вознаграждения и связанной привычки
        validate_reward_and_related_habit(self)

        # Проверка, что связанная привычка является приятной
        validate_related_habit_is_pleasant(self)
        