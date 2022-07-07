from django.urls import path

from api.schema import schema

from .views import PodcastGraphQLView


urlpatterns = [
    path("graphql", PodcastGraphQLView.as_view(schema=schema)),
]
