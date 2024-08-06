from celery import  shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from datetime import timedelta
from config.settings import EMAIL
from users.models import Subscription


@shared_task
def notify_subscribers(course_id):
    # Логика рассылки писем подписчикам курса
    course = Subscription.objects.get(course=course_id)
    for subscriber in course.subscribers.all():
        send_mail(
            subject=f'Уведомление о новом курсе "{course.name}"',
            message=f'Вы получили уведомление о новом курсе "{course.name}"',
            from_email=EMAIL,
            recipient_list=[subscriber.email]
        )


@shared_task
def disable_inactive_users():
    users = get_user_model().objects.filter(is_active=True)
    for user in users:
        if user.last_login < timedelta(days=30):
            user.is_active = False
            user.save()
