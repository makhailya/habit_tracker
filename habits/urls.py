from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitViewSet

app_name = "habits"

router = DefaultRouter()
router.register(r"my-habits", HabitViewSet, basename="habit")
router.register(r"public", PublicHabitViewSet, basename="public-habit")

urlpatterns = [
    path("", include(router.urls)),
]
