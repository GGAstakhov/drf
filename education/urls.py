# Импорт необходимых модулей
from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

# Импорт необходимых классов из views
from .views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    PaymentListAPIView,
    PaymentCreateAPIView
)

# Создание экземпляра DefaultRouter
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

# Получение имени приложения
app_name = EducationConfig.name

# Создание списка URL-шаблонов
urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
] + router.urls

