from django.core.mail import send_mail
from django.conf import settings


def send_message_active(email, course_name):
    send_mail(
        'Подписка',
        f'На курс {course_name} у вас оформлена подписка',
        settings.EMAIL_HOST_USER,
        [email]
    )
