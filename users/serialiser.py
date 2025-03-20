from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Payments, SubscriptionToCourse, User


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "avatar",
            "city",
            "password",
        ]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("password", None)
        return representation


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        return token


class SubscriptionToCourseSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionToCourse
        fields = "__all__"
