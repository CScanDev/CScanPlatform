from rest_framework.routers import DefaultRouter

from api.search.views import SearchView, TestAllCourseView

router = DefaultRouter()
router.register("", SearchView, basename="main")
router.register("test", TestAllCourseView, basename="test")
urlpatterns = router.urls
