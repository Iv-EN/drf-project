from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payments, User
from users.serialiser import (MyTokenObtainPairSerializer, PaymentSerializer,
                              UserDetailSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    """ViewSet для просмотра и изменения пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_queryset(self):
        """
        Возвращает всех пользователей для просмотра, и только текущего
        пользователя для редактирования.
        """
        if self.action in ["retrieve", "list"]:
            return User.objects.all()
        elif self.action in ["update", "partial_update", "destroy"]:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            serializer = UserDetailSerializer(instance)
        else:
            data = {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "phone_number": instance.phone_number,
                "city": instance.city,
            }
            return Response(data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            return Response(
                {"error": "У вас нет прав для редактирования этого профиля."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(
            self.object, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PaymentViewSet(ModelViewSet):
    """ViewSet для просмотра и изменения платежей."""

    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_lesson", "paid_course", "payment_method"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        """Ограничивает доступ к платежам только текущего пользователя."""
        user = self.request.user
        return Payments.objects.filter(user=user.id)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
