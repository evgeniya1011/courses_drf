from datetime import timedelta

from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from courses.models import Subscription, Course, Lesson


@shared_task
def send_course_update(course_item: Course):
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


@shared_task
def send_lesson_update(lesson: Lesson):
    course = Course.objects.get(pk=lesson.course_id)
    now = timezone.localtime(timezone.now())
    subscription = Subscription.objects.filter(lesson=course_id, is_active=True)
    if subscription:
        if lesson_item.date_update:
            if (now - lesson_item.date_update) > timedelta(hours=4):
                for sub in subscription:
                    print('урок обновился')
                    # send_mail(
                    #     'Обновление курса',
                    #     f'{course_item.title} был обновлен',
                    #     settings.EMAIL_HOST_USER,
                    #     [sub.user.email]
                    #
                # )
                lesson_item.date_update = now

    def perform_update(self, serializer):
        """
        Определяем порядок изменения урока
        """
        changed_lesson = serializer.save()
        date_time_now = datetime.now()  # получаем текущие дату и время
        moscow_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
        date_now = date_time_now.astimezone(moscow_timezone)  # устанавливаем текущую дату с учетом часового пояса

        # если дата последнего изменения урока существует, проверяем условие запуска отложенной задачи
        if changed_lesson.lesson_datetime_changing:

            # устанавливаем дату последнего изменения урока с учетом часового пояса
            lesson_last_change_date = changed_lesson.lesson_datetime_changing.astimezone(moscow_timezone)

            # если текущее время больше времени последнего изменения урока на количество часов
            if abs(date_now - lesson_last_change_date) > timedelta(hours=4):
                # запускаем отложенную задачу по информированию подписчиков курса о изменениях уроков курса
                subscriber_notice.delay(changed_lesson.course_id)

        # заносим текущие дату и время в последние изменения урока
        changed_lesson.lesson_datetime_changing = date_now
        changed_lesson.save()

