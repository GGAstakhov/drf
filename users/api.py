from users.serializers import UserSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


class UserRegistrationView(generics.CreateAPIView):
    """
    API для регистрации нового пользователя.

    Поля:
    - email: почта пользователя (уникальное поле);
    - password: пароль пользователя;

    Запросы:
    - POST: Создание нового пользователя. Ожидается передача данных пользователя в формате JSON.
    """

    # Настройка прав доступа для представления
    permission_classes = [AllowAny]  # Разрешение доступа для всех пользователей
    serializer_class = UserSerializer  # Использование класса сериализатора UserSerializer

    # Метод для обработки POST-запроса
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Создание объекта сериализатора с данными запроса
        if serializer.is_valid():  # Проверка валидности данных
            serializer.save()  # Сохранение данных
            return Response(serializer.data, status=HTTP_201_CREATED)  # Возврат успешного ответа с данными
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)  # Возврат ошибки с невалидными
