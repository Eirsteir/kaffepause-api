from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from graphene_django.views import GraphQLView

app_name = "api"
urlpatterns = [
    # https://docs.graphene-python.org/projects/django/en/latest/installation/#csrf-exempt
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
    url(r"^$", RedirectView.as_view(url="/"), name="default"),
]
