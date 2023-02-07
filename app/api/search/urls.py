from rest_framework.routers import DefaultRouter

from api.search.views import SearchView

router = DefaultRouter()
router.register("", SearchView, basename="main")
urlpatterns = router.urls
