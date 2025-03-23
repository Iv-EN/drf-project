from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson


class BaseTestCase(APITestCase):
    """Базовый тестовый класс."""

    def setUp(self):
        """Метод для инициализации тестов."""

        self.user = User.objects.create(
            username="test_user", email="test_email", password="test"
        )
        self.course = Course.objects.create(
            name="test_course", description="test description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test description",
            course=self.course,
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)


class TestCourse(BaseTestCase):
    """Тестирование модели курса."""

    def test_create_course(self):
        """Проверка создания нового курса."""
        data = {
            "name": "test_course_2",
            "description": "test description 2",
        }
        response = self.client.post("/courses/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.last().name, "test_course_2")
        self.assertEqual(
            Course.objects.last().description, "test description 2"
        )
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        """Проверка изменения курса."""
        data = {"name": "updated_course_name"}
        response = self.client.put(
            f"/courses/{self.course.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Course.objects.get(id=self.course.id).name, "updated_course_name"
        )
        self.assertEqual(
            Course.objects.get(id=self.course.id).description,
            "test description",
        )
        self.assertEqual(Course.objects.count(), 1)

    def test_list_course(self):
        """Проверка получения списка курсов."""
        self.maxDiff = None
        response = self.client.get("/courses/")
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": "test_course",
                    "description": "test description",
                    "picture": None,
                    "owner": self.user.pk,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "name": "test_lesson",
                            "description": "test description",
                            "picture": None,
                            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "subscription": "У Вас нет подписки на этот курс",
                }
            ],
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, result, f"Ожидалось: {result}, получено: {data}"
        )

    def test_retrieve_course(self):
        """Проверка получения курса по id."""
        response = self.client.get(f"/courses/{self.course.id}/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("name"), self.course.name)
        self.assertEqual(Course.objects.all().count(), 1)

    def test_delete_course(self):
        """Проверка удаления курса."""
        response = self.client.delete(f"/courses/{self.course.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)


class TestLesson(BaseTestCase):
    """Тестирование модели урока."""

    def test_create_lesson(self):
        """Проверка создания нового урока."""
        url = reverse("courses:lesson_create")
        data = {
            "name": "test_lesson_2",
            "description": "test lesson description 2",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.last().name, "test_lesson_2")
        self.assertEqual(
            Lesson.objects.last().description, "test lesson description 2"
        )
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        """Проверка изменения урока."""
        url = reverse("courses:lesson_update", args=(self.lesson.pk,))
        data = {"name": "updated_lesson_name"}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Lesson.objects.get(id=self.course.id).name, "updated_lesson_name"
        )
        self.assertEqual(
            Lesson.objects.get(id=self.course.id).description,
            "test description",
        )
        self.assertEqual(Course.objects.count(), 1)

    def test_list_lesson(self):
        """Проверка получения списка уроков."""
        self.maxDiff = None
        url = reverse("courses:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "test_lesson",
                    "description": "test description",
                    "picture": None,
                    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, result, f"Ожидалось: {result}, получено: {data}"
        )

    def test_retrieve_lesson(self):
        """Проверка получения урока по id."""
        url = reverse("courses:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("name"), self.lesson.name)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_delete_lesson(self):
        """Проверка удаления урока."""
        url = reverse("courses:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)
