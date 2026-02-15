"""
Celery задачи для отправки напоминаний о привычках.
"""
import logging
import asyncio
from datetime import datetime, timedelta
from celery import shared_task
from django.utils import timezone
from .models import Habit
from .telegram_bot import telegram_service

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder(habit_id):
    """
    Отправка напоминания о привычке через Telegram.

    :param habit_id: ID привычки
    """
    try:
        habit = Habit.objects.select_related('user', 'related_habit').get(
            id=habit_id
        )

        # Проверяем, есть ли у пользователя Telegram ID
        if not habit.user.telegram_chat_id:
            logger.warning(
                f"У пользователя {habit.user.email} "
                f"не указан telegram_chat_id"
            )
            return

        # Форматируем сообщение
        message = telegram_service.format_habit_reminder(habit)

        # Отправляем сообщение
        asyncio.run(
            telegram_service.send_message(
                chat_id=habit.user.telegram_chat_id,
                message=message
            )
        )

        logger.info(f"Напоминание о привычке {habit_id} отправлено")

    except Habit.DoesNotExist:
        logger.error(f"Привычка с ID {habit_id} не найдена")
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания: {e}")


@shared_task
def schedule_habit_reminders():
    """
    Планирование напоминаний для всех активных привычек.
    Эта задача должна запускаться периодически (например, каждый час).
    """
    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    # Находим привычки, для которых нужно отправить напоминание
    # в ближайший час
    hour_later = (now + timedelta(hours=1)).time()

    habits = Habit.objects.select_related('user').filter(
        user__telegram_chat_id__isnull=False,
        time__gte=current_time,
        time__lt=hour_later
    )

    for habit in habits:
        # Проверяем периодичность
        # Здесь можно добавить логику проверки, что привычку
        # нужно выполнить сегодня

        # Планируем отправку напоминания в указанное время
        eta = timezone.make_aware(
            datetime.combine(current_date, habit.time)
        )

        if eta > now:
            send_habit_reminder.apply_async(
                args=[habit.id],
                eta=eta
            )
            logger.info(
                f"Запланировано напоминание для привычки "
                f"{habit.id} на {eta}"
            )
            