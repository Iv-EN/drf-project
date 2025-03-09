from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "picture", "lessons_count")

    def get_lessons_count(self, instance):
        return instance.lessons.count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
