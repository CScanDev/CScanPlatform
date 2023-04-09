from rest_framework.routers import DefaultRouter

from api.dashboard.views import DashboardView

router = DefaultRouter()
router.register("", DashboardView, basename="dashboard")
urlpatterns = router.urls
