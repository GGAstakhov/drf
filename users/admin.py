from django.contrib import admin

from users.models import User

# Добавляем в админку модель User
admin.site.register(User)
