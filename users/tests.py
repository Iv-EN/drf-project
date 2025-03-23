from rest_framework.fields import DateTimeField, DecimalField

from courses.tests import BaseTestCase
from .models import Payments, SubscriptionToCourse, User


class TestUser(BaseTestCase):
    """Тестирование модели курса."""

    def test_create_user(self):
        """Проверка создания нового пользователя."""

        data = {
            "username": "new_test_user",
            "email": "test@email.ru",
            "password": "test",
        }
        response = self.client.post("/users/user/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.last().username, "new_test_user")
        self.assertEqual(User.objects.last().email, "test@email.ru")
        self.assertEqual(User.objects.count(), 2)

    def test_list_users(self):
        """Проверка получения списка всех пользователей."""

        response = self.client.get("/users/user/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_retrieve_user(self):
        """Проверка получения конкретного пользователя."""

        response = self.client.get(f"/users/user/{self.user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "test_user")
        self.assertEqual(response.data["email"], "test_email")
        self.assertEqual(response.data["id"], self.user.id)

    def test_update_user(self):
        """Проверка изменения пользователя."""

        data = {"username": "updated_test_user"}
        response = self.client.put(f"/users/user/{self.user.id}/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.get(id=self.user.id).username, "updated_test_user"
        )
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user(self):
        """Проверка удаления пользователя."""

        response = self.client.delete(f"/users/user/{self.user.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)


class TestPayments(BaseTestCase):
    """Тестирование модели оплаты."""

    def setUp(self):
        super().setUp()
        self.payment = Payments.objects.create(
            user=self.user,
            paid_lesson=self.lesson,
            paid_course=self.course,
            amount=100,
            payment_method="cash",
        )

    def test_create_payment(self):
        """Проверка создания новой оплаты."""

        data = {
            "user": self.user.pk,
            "amount": 10000,
            "paid_lesson": self.lesson.pk,
            "paid_course": self.course.pk,
            "payment_method": "bank_transfer",
        }
        response = self.client.post(f"/users/payment/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payments.objects.count(), 2)
        self.assertEqual(Payments.objects.last().amount, 10000)
        self.assertEqual(
            Payments.objects.last().payment_method, "bank_transfer"
        )

    def test_list_payment(self):
        """Проверка получения списка всех оплат."""

        res_created_at = DateTimeField().to_representation
        res_payment_amount = DecimalField(
            decimal_places=2,
            max_digits=9,
        ).to_representation
        response = self.client.get("/users/payment/")
        data = response.json()
        result = [
            {
                "id": self.payment.pk,
                "user": self.user.pk,
                "created_at": res_created_at(self.payment.created_at),
                "amount": res_payment_amount(self.payment.amount),
                "paid_lesson": self.lesson.pk,
                "paid_course": self.course.pk,
                "payment_method": self.payment.payment_method,
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Payments.objects.count(), 1)
        self.assertEqual(data, result)

    def test_retrieve_payment(self):
        """Проверка получения конкретной оплаты."""

        response = self.client.get(f"/users/payment/{self.payment.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.payment.pk)
        self.assertEqual(response.data["user"], self.user.pk)
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["paid_lesson"], self.lesson.pk)
        self.assertEqual(response.data["paid_course"], self.course.pk)
        self.assertEqual(response.data["payment_method"], "cash")

    def test_update_payment(self):
        """Проверка изменения оплаты."""

        data = {
            "user": self.user.pk,
            "amount": 200,
            "paid_lesson": self.lesson.pk,
            "paid_course": self.course.pk,
            "payment_method": "bank_transfer",
        }
        response = self.client.put(
            f"/users/payment/{self.payment.pk}/", data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Payments.objects.get(id=self.payment.pk).payment_method,
            "bank_transfer",
        )
        self.assertEqual(Payments.objects.get(id=self.payment.pk).amount, 200)
        self.assertEqual(Payments.objects.count(), 1)

    def test_delete_payment(self):
        """Проверка удаления оплаты."""

        response = self.client.delete(f"/users/payment/{self.payment.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Payments.objects.count(), 0)


class TestSubscriptionToCourse(BaseTestCase):
    """Тестирование подписки на курс."""

    def test_subscriptionToCourse(self):
        """Проверка создания подписки на курс."""

        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post("/users/subscription/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SubscriptionToCourse.objects.count(), 1)
        self.assertEqual(
            SubscriptionToCourse.objects.last().user.pk, self.user.pk
        )
        self.assertEqual(
            SubscriptionToCourse.objects.last().course.pk, self.course.pk
        )
        self.assertEqual(
            response.json(), f"Вы подписались на курс '{self.course.name}'."
        )

    def test_un_subscriptionToCourse(self):
        """Проверка отписки от курса."""

        self.subscription = SubscriptionToCourse.objects.create(
            course=self.course, user=self.user
        )
        data = {"user": self.user.id, "course": self.course.id}
        response = self.client.post("/users/subscription/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), f"Вы отписались от курса '{self.course.name}'."
        )
