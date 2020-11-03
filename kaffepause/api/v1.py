from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from kaffepause.users.views import UserViewSet, UserCreateViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
