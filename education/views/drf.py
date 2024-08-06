from rest_framework import viewsets, generics, filters
from education import serializers
from education.models import Course, Lesson, Payment
from education.serializers import PaymentSerializer, SubscriptionSerializer, PaymentCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from users.models import ModeratorPermissions, IsOwner, Subscription
from education.tasks import notify_subscribers


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    """
    API для работы с курсами.

    Разрешения:
    - Создание и удаление курса доступно только модераторам.
    - Редактирование и просмотр доступны только модераторам и владельцам курса.

    Поля:
    - serializer_class: Класс сериализатора для курса.
    - permission_classes: Классы разрешений для доступа к API.
    - perform_create: Метод для сохранения владельца курса при создании.

    Методы:
    - get_permissions: Переопределенный метод для настройки разрешений в зависимости от действия.

    Запросы:
    - GET: Получение списка курсов.
    - POST: Создание нового курса.
    - GET (/:id): Получение конкретного курса.
    - PUT (/:id): Обновление информации о курсе.
    - DELETE (/:id): Удаление курса.
    """
    serializer_class = serializers.CourseSerializer
    permission_classes = [ModeratorPermissions | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [~ModeratorPermissions]
        # Редактировать и просматривать могут только модераторы и владельцы
        if self.action in ['update', 'retrieve']:
            self.permission_classes = [ModeratorPermissions | IsOwner]
        return super(CourseViewSet, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user).order_by('id')


# API для создания урока
class LessonCreateAPIView(generics.ListCreateAPIView):
    """
    API для создания урока.

    Разрешения:
    - Создание доступно только пользователям, не являющимся модераторами.

    Поля:
    - serializer_class: Класс сериализатора для урока.
    - queryset: Запрос для получения списка уроков.
    - permission_classes: Классы разрешений для доступа к API.
    - perform_create: Метод для сохранения владельца урока при создании.

    Запросы:
    - GET: Получение списка уроков.
    - POST: Создание нового урока.
    """
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.order_by('id')
    permission_classes = [~ModeratorPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# API для получения списка уроков
class LessonListAPIView(generics.ListAPIView):
    """
    API для получения списка уроков.

    Разрешения:
    - Просмотр доступен только модераторам и владельцам уроков.

    Поля:
    - serializer_class: Класс сериализатора для урока.
    - queryset: Запрос для получения списка уроков.
    - permission_classes: Классы разрешений для доступа к API.

    Запросы:
    - GET: Получение списка уроков.
    """
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.order_by('id')
    permission_classes = [ModeratorPermissions | IsOwner]


# API для получения конкретного урока
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    API для получения конкретного урока.

    Разрешения:
    - Просмотр доступен только модераторам и владельцам уроков.

    Поля:
    - serializer_class: Класс сериализатора для урока.
    - queryset: Запрос для получения всех уроков.
    - permission_classes: Классы разрешений для доступа к API.

    Запросы:
    - GET: Получение конкретного урока.
    """
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermissions | IsOwner]


# API для обновления урока
class LessonUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API для обновления урока.

    Разрешения:
    - Редактирование доступно только модераторам и владельцам уроков.

    Поля:
    - serializer_class: Класс сериализатора для урока.
    - queryset: Запрос для получения всех уроков.
    - permission_classes: Классы разрешений для доступа к API.

    Запросы:
    - GET: Получение конкретного урока.
    - PUT: Обновление информации о уроке.
    """
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermissions | IsOwner]


# API для удаления урока
class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления урока.

    Разрешения:
    - Удаление доступно только модераторам и владельцам уроков.

    Поля:
    - queryset: Запрос для получения всех уроков.
    - permission_classes: Классы разрешений для доступа к API.

    Запросы:
    - DELETE: Удаление урока.
    """
    queryset = Lesson.objects.all()
    permission_classes = [~ModeratorPermissions | IsOwner]


# API для получения списка платежей
class PaymentListAPIView(generics.ListAPIView):
    """
    API для получения списка платежей.

    Разрешения:
    - Просмотр доступен только модераторам и владельцам платежей.

    Поля:
    - serializer_class: Класс сериализатора для платежа.
    - queryset: Запрос для получения всех платежей.
    - filter_backends: Классы фильтрации и сортировки.
    - ordering_fields: Поля, по которым можно сортировать.
    - filterset_fields: Поля, по которым можно фильтровать.
    - permission_classes: Классы разрешений для доступа к API.

    Запросы:
    - GET: Получение списка платежей.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['payment_date']
    filterset_fields = ['course', 'lesson', 'payment_method']
    permission_classes = [ModeratorPermissions | IsOwner]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        course = serializer.save(user=self.request.user)
        notify_subscribers.delay(course.id)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)