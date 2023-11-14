from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def user_block():
    now = timezone.localtime(timezone.now())
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login:
            if (now - user.last_login) > timedelta(days=30):
                user.is_active = False
                user.save()
        else:
            send_mail(
                'Важная информация',
                'Для сохраннеия авторизации на сайте обновите данные',
                settings.EMAIL_HOST_USER,
                [user.email]
            )
