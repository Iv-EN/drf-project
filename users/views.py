from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.serialiser import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    """ViewSet для просмотра и изменения пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
    """ViewSet для просмотра и изменения платежей."""

    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_lesson", "paid_course", "payment_method"]
    ordering_fields = ["created_at"]
