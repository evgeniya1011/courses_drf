from django.core.management import BaseCommand

from courses.models import Payments, Course, Lesson
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Payments.objects.all().delete()

        payments_list = [
            {'user': User.objects.get(pk=3), 'date_payment': '2023-10-05', 'course': Course.objects.get(pk=2), 'amount': "150000", 'method': 'cash'},
            {'user': User.objects.get(pk=2), 'date_payment': '2022-08-05', 'course': Course.objects.get(pk=3), 'amount': "125000"},
            {'user': User.objects.get(pk=2), 'date_payment': '2023-07-11', 'lesson': Lesson.objects.get(pk=3), 'amount': "52000", 'method': 'cash'},
            {'user': User.objects.get(pk=3), 'date_payment': '2023-05-25', 'lesson': Lesson.objects.get(pk=1), 'amount': "25000", 'method': 'cash'}
        ]

        payments_for_create = []
        for payment in payments_list:
            payments_for_create.append(Payments(**payment))
        Payments.objects.bulk_create(payments_for_create)

