from rest_framework.routers import DefaultRouter

from api.search.views import SearchView, TestView

router = DefaultRouter()
router.register("", SearchView, basename="main")
router.register("test", TestView, basename="test")
urlpatterns = router.urls
