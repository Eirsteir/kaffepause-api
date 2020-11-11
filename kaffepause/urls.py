from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from kaffepause.api import urls as api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^", include(api_urls, namespace="api")),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
