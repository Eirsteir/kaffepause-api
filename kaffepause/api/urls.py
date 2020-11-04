from django.conf import settings
from django.conf.urls import url
from django.urls import include
from django.views.generic import RedirectView

from kaffepause.api.v1 import router as v1

app_name = "api"
urlpatterns = [
    url(r"^v1/", include((v1.urls, "v1"), namespace="v1")),
    url(
        r"^$", RedirectView.as_view(url=f"/api/{settings.API_VERSION}/"), name="default"
    ),
]
