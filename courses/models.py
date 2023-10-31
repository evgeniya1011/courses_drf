from config import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


PAYMENT_CHOICES = (
    ('transfer to account', 'перевод на счет'),
    ('cash', 'наличные')
)


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    picture = models.ImageField(upload_to='course/', verbose_name='Изображение', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='lesson/', verbose_name='Изображение', **NULLABLE)
    url = models.URLField(max_length=250, verbose_name='ссылка', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE, related_name='lesson')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE, related_name='payment')
    date_payment = models.DateField(verbose_name='Дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    amount = models.CharField(max_length=50, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='transfer to account', verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.course if self.course else self.lesson}:{self.amount} - {self.method}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Подписка')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='subscription')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.course} - {self.is_active}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
