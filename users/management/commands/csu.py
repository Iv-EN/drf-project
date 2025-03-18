from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создает нового пользователя."

    def handle(self, *args, **options):
        user = User.objects.create_user(
            username="admin",
            email="admin@admin.ru",
            password="admin",
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Супер пользователь '{user.username}' создан.")
        )
