from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "picture",
            "lessons_count",
            "lessons",
        )

    def get_lessons_count(self, instance):
        return instance.lessons.count()
