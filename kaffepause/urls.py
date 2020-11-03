from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from rest_framework.authtoken import views

from kaffepause.api.urls import urlpatterns as api

auth_urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^api/", include("kaffepause.api.urls", namespace="api")),
    url(r"^auth/", include(auth_urlpatterns)),
    url(
        r"^api-docs/",
        include_docs_urls(
            title=settings.SITE["name"],
            description=settings.SITE["slogan"],
            patterns=api,
            schema_url="/api",
        ),
    ),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
