from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from courses.models import Subscription, Course


@shared_task
def send_message_update(course_item: Course):
    course = Course.objects.get(pk=course_item.pk)
    subscription = Subscription.objects.filter(course=course_item.pk, is_active=True)
    if subscription:
        for sub in subscription:
            print('курс обновился')
            # send_mail(
            #     'Обновление курса',
            #     f'{course_item.title} был обновлен',
            #     settings.EMAIL_HOST_USER,
            #     [sub.user.email]
            #
            # )
