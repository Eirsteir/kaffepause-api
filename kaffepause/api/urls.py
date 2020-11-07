from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from graphene_django.views import GraphQLView

from kaffepause.api.api_router import router

app_name = "api"
urlpatterns = [
    url(r"^", include((router.urls, "v1"), namespace="v1")),
    path(
        "graphql", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))
    ),  # TODO: remove csrf_exempt
    url(r"^$", RedirectView.as_view(url="/"), name="default"),
]
