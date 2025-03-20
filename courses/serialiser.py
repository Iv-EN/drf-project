from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import SubscriptionToCourse

from .models import Course, Lesson
from .validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "video_url": {
                "validators": [VideoLinkValidator(field="video_url")]
            }
        }


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "picture",
            "owner",
            "lessons_count",
            "lessons",
            "subscription",
        )

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def create(self, validated_data):
        lessons_data = validated_data.pop("lessons", None)
        course = Course.objects.create(**validated_data)
        if lessons_data:
            for lesson_data in lessons_data:
                Lesson.objects.create(course=course, **lesson_data)
        return course

    def get_subscription(self, instance):
        user = self.context["request"].user
        subscription = (
            SubscriptionToCourse.objects.all()
            .filter(user=user, course=instance)
            .exists()
        )
        if subscription:
            return "Вы подписаны на этот курс"
        return "У Вас нет подписки на этот курс"
