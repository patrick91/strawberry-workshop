from django.urls import path
from django.views.generic.base import RedirectView

from api.schema import schema

from .views import PodcastGraphQLView


urlpatterns = [
    path("graphql", PodcastGraphQLView.as_view(schema=schema)),
    path("", RedirectView.as_view(url="/graphql")),
]
