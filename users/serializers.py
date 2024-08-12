from rest_framework import serializers
from users.models import User


# Сериализатор пользователей
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Поле для пароля, доступное только для записи

    class Meta:
        model = User  # Используемая модель
        fields = ['email', 'password']  # Поля для сериализации

    def create(self, validated_data):
        password = validated_data.pop('password')  # Извлечение пароля из валидированных данных
        user = User(**validated_data)  # Создание нового пользователя с остальными данными
        user.set_password(password)  # Установка зашифрованного пароля
        user.save()  # Сохранение пользователя в базе данных
        return user  # Возврат созданного пользователя
