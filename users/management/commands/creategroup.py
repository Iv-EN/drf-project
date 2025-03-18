from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.apps import UsersConfig


class Command(BaseCommand):
    def handle(self, *args, **options):

        def print_group_status(name, status):
            print(
                f'Группа модераторов "{name}" -',
                "создана" if status else "уже существует",
            )

        _, created_manager_group = Group.objects.get_or_create(
            name=UsersConfig.moderator_group_name
        )
        print_group_status(
            UsersConfig.moderator_group_name, created_manager_group
        )
