import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from courses.models import Course

from .models import Payments, SubscriptionToCourse, User
from .serialiser import (MyTokenObtainPairSerializer, PaymentSerializer,
                         SubscriptionToCourseSerializer, UserDetailSerializer,
                         UserSerializer)
from .services import create_stripe_price, create_stripe_product, \
    create_stripe_session


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

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(product_id, payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

    @action(detail=True, methods=["get"])
    def check_payment_status(self, request, pk=None):
        """Проверяет статус платежа по session_id."""
        try:
            payment = self.get_object()
            session_id = payment.session_id
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                payment.status = "Оплачен"
            else:
                payment.status = "Не оплачен"
            payment.save()
            return Response(
                payment.status, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubscriptionToCourseView(APIView):
    """ViewSet для подписки/отписки на курс."""

    queryset = SubscriptionToCourse.objects.all()
    serializer_class = SubscriptionToCourseSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = SubscriptionToCourse.objects.all().filter(
            user=user, course=course_item
        )
        if subs_item.exists():
            subs_item.delete()
            message = f"Вы отписались от курса '{course_item.name}'."
        else:
            SubscriptionToCourse.objects.create(user=user, course=course_item)
            message = f"Вы подписались на курс '{course_item.name}'."
        return Response(message, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
