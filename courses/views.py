from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from users.apps import UsersConfig
from users.permissions import IsModerator, IsNotModerator, IsOwner

from .models import Course, Lesson
from .paginators import CoursesPaginator, LessonsPaginator
from .serialiser import CourseSerializer, LessonSerializer
from .services import get_data_for_sending_messages
from .tasks import send_update_course


class CourseViewSet(ModelViewSet):
    """Viewset для курсов."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = CoursesPaginator

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
    """Базовый класс для всех viewsets уроков."""

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.groups.filter(
            name=UsersConfig.moderator_group_name
        ).exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonApiViewMixin:
    """Миксин для viewsets уроков."""

    def handle_course_update(self, lesson, change):
        if lesson.course:
            if lesson.course.updated_at < timezone.now() - timedelta(hours=4):
                lesson.course.updated_at = timezone.now()
                lesson.course.save()
                subscribers_mail, message, subject = (
                    get_data_for_sending_messages(lesson, change=change)
                )
                send_update_course.delay(
                    subscribers_mail=subscribers_mail,
                    message=message,
                    subject=subject,
                )


class LessonCreateApiView(BaseApiView, CreateAPIView, LessonApiViewMixin):
    """Создание нового урока."""

    permission_classes = (IsNotModerator,)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        self.handle_course_update(lesson, change="created")


class LessonListApiView(BaseApiView, ListAPIView):
    """Получение списка уроков."""

    pagination_class = LessonsPaginator


class LessonRetieveApiView(BaseApiView, RetrieveAPIView):
    """Получение информации о конкретном уроке."""

    permission_classes = (IsModerator | IsOwner,)


class LessonUpdateApiView(BaseApiView, UpdateAPIView, LessonApiViewMixin):
    """Обновление информации о конкретном уроке."""

    permission_classes = (IsModerator | IsOwner,)

    def perform_update(self, serializer):
        lesson = serializer.save()
        self.handle_course_update(lesson, change="updated")


class LessonDestroyApiView(BaseApiView, DestroyAPIView, LessonApiViewMixin):
    """Удаление конкретного урока."""

    permission_classes = (IsNotModerator | IsOwner,)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.handle_course_update(instance, change="deleted")
