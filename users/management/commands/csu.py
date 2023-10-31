from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin11@mail.ru',
            first_name='Test',
            last_name='Testov',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('123qwer456ty')
        user.save()
