from rest_framework.routers import DefaultRouter

from apps.arena.api.v1.views import FootballArenaViewSet

router = DefaultRouter()
router.register("", FootballArenaViewSet)

urlpatterns = []
urlpatterns += router.urls
