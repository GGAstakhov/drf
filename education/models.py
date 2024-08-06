from django.db import models

from config import settings
from src.constants import NULLABLE
from django.conf import settings


# Класс модели "Курс": название, превью (картинка), описание
class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    image = models.ImageField(upload_to='courses', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    # дата и время создания курса
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    # привязка к пользователю
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        **NULLABLE
    )

    def __str__(self):
        return self.name


# Класс модели "Урок": курс, название, описание, превью (картинка), ссылка на видео
class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='lesson', **NULLABLE, verbose_name='первью')
    video_url = models.URLField(**NULLABLE, verbose_name='видео')
    # дата и время создания урока
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    # привязка к пользователю
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        **NULLABLE
    )

    def __str__(self):
        return self.title


# Класс модели платежей
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    payment_date = models.DateField(verbose_name='дата оплаты', auto_now_add=True)
    # оплаченный курс
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    # оплаченный урок
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты', **NULLABLE)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Наличные'),
            ('transfer', 'Перевод на счет')
        ],
        verbose_name='способ оплаты',
        default='transfer'
    )

    def __str__(self):
        return f'{self.user} - {self.course} - {self.lesson}'
