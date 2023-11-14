from datetime import timedelta

from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from courses.models import Subscription, Course, Lesson


@shared_task
def send_course_update(course_id: int):
    course = Course.objects.get(pk=course_id)
    subscription = Subscription.objects.filter(course=course.pk, is_active=True)
    if subscription:
        for sub in subscription:
            send_mail(
                'Обновление курса',
                f'{course.title} был обновлен',
                settings.EMAIL_HOST_USER,
                [sub.user.email]

            )


@shared_task
def send_lesson_update(course_id, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    course = Course.objects.get(pk=course_id)
    now = timezone.localtime(timezone.now())
    subscription = Subscription.objects.filter(course=course.pk, is_active=True)
    if subscription:
        if lesson.date_update:
            if (now - lesson.date_update) > timedelta(hours=4):
                for sub in subscription:
                    send_mail(
                        'Обновление материалов курса',
                        f'В курсе {course.title} был обновлен урок {lesson.title}',
                        settings.EMAIL_HOST_USER,
                        [sub.user.email]
                    )
    lesson.date_update = now
    lesson.save()
