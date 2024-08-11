# Импорт базового класса для команд Django
from django.core.management import BaseCommand
# Импорт модели User
from users.models import User


# Определение класса Command
class Command(BaseCommand):
    # Определение метода handle, который будет выполняться при вызове команды
    def handle(self, *args, **options):
        # Создание пользователя с предопределенными значениями
        user = User.objects.create(
            first_name='admin',  # Установка имени пользователя
            email='admin@sky.pro',  # Установка электронной почты пользователя
            last_name='SkyPro',  # Установка фамилии пользователя
            is_superuser=True,  # Установка статуса суперпользователя
            is_staff=True,  # Установка статуса сотрудника
        )
        # Установка пароля для пользователя
        user.set_password('admin')
        # Сохранение изменений в базе данных
        user.save()
