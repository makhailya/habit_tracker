from django.core.exceptions import ValidationError


def validate_execution_time(value):
    """
    Валидатор времени выполнения привычки.
    Время выполнения не должно превышать 120 секунд.
    """
    if value > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_periodicity(value):
    """
    Валидатор периодичности выполнения привычки.
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    if value < 1:
        raise ValidationError("Периодичность должна быть не менее 1 дня.")
    if value > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")


def validate_pleasant_habit(habit):
    """
    Валидатор для приятной привычки.
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """
    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if habit.related_habit:
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки."
            )


def validate_reward_and_related_habit(habit):
    """
    Валидатор для исключения одновременного выбора связанной привычки
    и вознаграждения.
    """
    if habit.reward and habit.related_habit:
        raise ValidationError(
            "Нельзя одновременно указать вознаграждение и связанную привычку. "
            "Выберите что-то одно."
        )


def validate_related_habit_is_pleasant(habit):
    """
    Валидатор для проверки, что связанная привычка является приятной.
    """
    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError(
            "В связанные привычки могут попадать только привычки "
            "с признаком приятной привычки."
        )
