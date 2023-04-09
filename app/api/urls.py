from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="1.0.0",
        description="",
        # TODO разобраться почему не рисуется API при ограниченных юзерах
        # permission_classes=(IsAdminUser,)
    ),
)

urlpatterns = [
    path("api/", include("api.search.urls")),
    path("api/", include("api.dashboard.urls")),
    path("api/swagger/", schema_view.with_ui("swagger")),
]
