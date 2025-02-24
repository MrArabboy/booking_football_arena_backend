from django.urls import include, path

urlpatterns = [
    path("v1/booking/", include("apps.booking.api.v1.urls")),
]
