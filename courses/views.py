from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson
from courses.serialiser import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """Viewset для просмотра курсов."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class BaseApiView:
    """Базовый класс для всех viewsets."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class LessonCreateApiView(BaseApiView, CreateAPIView):
    """Создание нового урока курса."""


class LessonListApiView(BaseApiView, ListAPIView):
    """Получение списка уроков курса."""


class LessonRetieveApiView(BaseApiView, RetrieveAPIView):
    """Получение информации о конкретном уроке курса."""


class LessonUpdateApiView(BaseApiView, UpdateAPIView):
    """Обновление информации о конкретном уроке курса."""


class LessonDestroyApiView(BaseApiView, DestroyAPIView):
    """Удаление конкретного урока курса."""
