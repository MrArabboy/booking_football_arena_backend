from rest_framework.routers import DefaultRouter

from apps.booking.api.v1.views import BookingViewSet

router = DefaultRouter()
router.register("", BookingViewSet)

urlpatterns = []

urlpatterns += router.urls
