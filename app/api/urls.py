from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="1.0.0",
        description=""
    ),
    public=True
)

urlpatterns = [
    path("api/", include("api.search.urls")),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]
