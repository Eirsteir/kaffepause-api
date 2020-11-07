from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from kaffepause.users.views import UserCreateViewSet, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)
