from django.urls import include, path

urlpatterns = [
    path("v1/arena/", include("apps.arena.api.v1.urls")),
]
