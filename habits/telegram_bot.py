"""
Интеграция с Telegram для отправки напоминаний о привычках.
"""

import logging

from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramService:
    """
    Сервис для работы с Telegram Bot API.
    """

    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.bot = None
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)

    async def send_message(self, chat_id, message):
        """
        Отправка сообщения в Telegram.

        :param chat_id: ID чата для отправки
        :param message: Текст сообщения
        :return: True если успешно, False если ошибка
        """
        if not self.bot:
            logger.error("Telegram bot token не настроен")
            return False

        try:
            await self.bot.send_message(
                chat_id=chat_id, text=message, parse_mode="HTML"
            )
            logger.info(f"Сообщение отправлено в чат {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            return False

    def format_habit_reminder(self, habit):
        """
        Форматирование напоминания о привычке.

        :param habit: Объект привычки
        :return: Отформатированное сообщение
        """
        message = "🔔 <b>Напоминание о привычке!</b>\n\n"
        message += f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        message += f"📍 Место: {habit.place}\n"
        message += f"✨ Действие: {habit.action}\n"
        message += f"⏱ Время на выполнение: {habit.execution_time} сек.\n"

        if habit.reward:
            message += f"\n🎁 Вознаграждение: {habit.reward}"
        elif habit.related_habit:
            message += f"\n😊 После выполнения: {habit.related_habit.action}"

        return message


# Создаем экземпляр сервиса
telegram_service = TelegramService()
