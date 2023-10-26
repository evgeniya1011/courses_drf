from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin1@mail.ru',
            first_name='Administator',
            last_name='Administator',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('123qwer456ty')
        user.save()
