from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from graphene_django.views import GraphQLView

app_name = "api"
urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=settings.DEBUG)),
    url(r"^$", RedirectView.as_view(url="/"), name="default"),
]
