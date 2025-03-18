from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson
from courses.serialiser import CourseSerializer, LessonSerializer
from users.apps import UsersConfig
from users.permissions import IsModerator, IsNotModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """Viewset для курсов."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_queryset(self):
        if (
            self.action != "list"
            or self.request.user.groups.filter(
                name=UsersConfig.moderator_group_name
            ).exists()
        ):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsNotModerator,)
        elif self.action == "destroy":
            self.permission_classes = (IsNotModerator | IsOwner,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()


class BaseApiView:
    """Базовый класс для всех viewsets."""

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.groups.filter(
            name=UsersConfig.moderator_group_name
        ).exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonCreateApiView(BaseApiView, CreateAPIView):
    """Создание нового урока курса."""

    permission_classes = (IsNotModerator,)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)


class LessonListApiView(BaseApiView, ListAPIView):
    """Получение списка уроков курса."""


class LessonRetieveApiView(BaseApiView, RetrieveAPIView):
    """Получение информации о конкретном уроке курса."""

    permission_classes = (IsModerator | IsOwner,)


class LessonUpdateApiView(BaseApiView, UpdateAPIView):
    """Обновление информации о конкретном уроке курса."""

    permission_classes = (IsModerator | IsOwner,)


class LessonDestroyApiView(BaseApiView, DestroyAPIView):
    """Удаление конкретного урока курса."""

    permission_classes = (IsNotModerator | IsOwner,)
