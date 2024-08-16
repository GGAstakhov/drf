# Импортируем необходимые модули и модели
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from .models import Course, Lesson
from users.models import Subscription, User


# Создаем тестовый случай для курса
class CourseTestCase(APITestCase):
    # Настраиваем начальные условия для тестов
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='UserTest',  # Установка имени пользователя
            email='user_test@sky.pro',  # Установка электронной почты пользователя
            last_name='Test',  # Установка фамилии пользователя
            is_superuser=False,  # Установка статуса суперпользователя
            is_staff=False,  # Установка статуса сотрудника
        )
        self.user.set_password('user_test')
        self.url = '/courses/'
        self.data = {"name": "New Course"}

        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(name="Test Course", owner=self.user)

    # Тестируем создание курса и просмотр курса
    def test_course_create(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 201)

    # Тестируем просмотр курса
    def test_course_retrieve(self):
        response = self.client.get(f'{self.url}{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.course.name)

    # Тестируем список курсов
    def test_course_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Предполагаем, что в базе данных 1 курс от текущего пользователя
        self.assertEqual(Course.objects.count(), 1)

    # Тестируем обновление курса
    def test_course_update(self):
        response = self.client.put(f'{self.url}{self.course.id}/', {'name': 'Updated Course'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Course')
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, 'Updated Course')


# Создаем тестовый случай для урока
class LessonTestCase(TestCase):
    # Настраиваем начальные условия для тестов
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='UserTest',  # Установка имени пользователя
            email='user_test@sky.pro',  # Установка электронной почты пользователя
            last_name='Test',  # Установка фамилии пользователя
            is_superuser=False,  # Установка статуса суперпользователя
            is_staff=False,  # Установка статуса сотрудника
        )
        self.user.set_password('user_test')
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(name="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, owner=self.user)

    # Тестируем список уроков
    def test_lesson_list(self):
        response = self.client.get(f'/lessons/?course={self.course.id}')
        self.assertEqual(response.status_code, 200)
        # Предполагаем, что в базе данных только один урок
        self.assertEqual(Lesson.objects.count(), 1)

    # Тестируем получение информации об уроке
    def test_lesson_retrieve(self):
        response = self.client.get(f'/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.lesson.title)

    # Тестируем обновление урока
    def test_lesson_update(self):
        response = self.client.put(f'/lessons/update/{self.lesson.id}/', {'title': 'Updated Lesson'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Lesson')
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    # Тестируем удаление урока
    def test_lesson_delete(self):
        response = self.client.delete(f'/lessons/delete/{self.lesson.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


# Создаем тестовый случай для подписки
class SubscriptionTestCase(TestCase):
    # Настраиваем начальные условия для тестов
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='UserTest',  # Установка имени пользователя
            email='user_test@sky.pro',  # Установка электронной почты пользователя
            last_name='Test',  # Установка фамилии пользователя
            is_superuser=False,  # Установка статуса суперпользователя
            is_staff=False,  # Установка статуса сотрудника
        )
        self.user.set_password('user_test')
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(name="Test Course", owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course)

    # Тестируем список подписок
    def test_subscription_list(self):
        response = self.client.get(f'/users/subscriptions/?course={self.course.id}')
        self.assertEqual(response.status_code, 200)
        # Предполагаем, что в базе данных 4 подписки
        self.assertEqual(Subscription.objects.count(), 1)

    # Тестируем создание подписки
    def test_subscription_create(self):
        response = self.client.post('/users/subscriptions/', {'course': self.course.id})
        self.assertEqual(response.status_code, 201)

    # Тестируем удаление подписки
    def test_subscription_delete(self):
        response = self.client.delete(f'/users/subscriptions/{self.subscription.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Subscription.objects.filter(id=self.subscription.id).exists())
