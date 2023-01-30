from django.contrib import admin
from django.urls import path, include
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
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0))
]
