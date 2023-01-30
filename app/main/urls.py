from rest_framework.routers import DefaultRouter

from main.views import MainView

router = DefaultRouter()
router.register("", MainView, basename="main")
urlpatterns = router.urls


