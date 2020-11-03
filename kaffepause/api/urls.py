from django.conf.urls import url
from django.urls import re_path, include, reverse_lazy
from django.views.generic import RedirectView

from kaffepause.api.v1 import router as v1

app_name = "api"
urlpatterns = [
    url(r"^v1/", include((v1.urls, "v1"), namespace="v1")),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
]

