from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from education.views import SubscriptionViewSet, SubscriptionCreateAPIView, SubscriptionDestroyAPIView
from users.api import UserRegistrationView
from users.apps import UsersConfig

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),  # Регистрация пользователя

    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
] + router.urls
