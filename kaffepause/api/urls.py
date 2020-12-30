from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from graphene_file_upload.django import FileUploadGraphQLView

app_name = "api"
urlpatterns = [
    url(r"^$", RedirectView.as_view(url="/"), name="default"),
]

# Disable CSRF protection only if we're in development mode.
# https://docs.graphene-python.org/projects/django/en/latest/installation/#csrf-exempt
if settings.DEBUG:
    urlpatterns.append(
        path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True)))
    )
else:
    urlpatterns.append(path("graphql/", FileUploadGraphQLView.as_view(graphiql=False)))
