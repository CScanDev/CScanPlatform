from django.contrib import admin
from django.urls import path, include

app_name = "app"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/",
        include(
            ("django.contrib.auth.urls", "accounts"),
            namespace="accounts"
        )
    ),
    path("", include("api.urls")),
]
