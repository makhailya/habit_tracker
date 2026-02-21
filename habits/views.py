from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Habit
from .permissions import IsOwner
from .serializers import HabitSerializer, PublicHabitSerializer


class HabitPagination(PageNumberPagination):
    """
    Пагинация для списка привычек.
    """

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления привычками пользователя.
    Пользователь может видеть только свои привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя.
        """
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Автоматически устанавливает текущего пользователя при создании.
        """
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра публичных привычек.
    Все пользователи могут видеть публичные привычки, но не могут их изменять.
    """

    serializer_class = PublicHabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """
        Возвращает только публичные привычки.
        """
        return Habit.objects.filter(is_public=True)
