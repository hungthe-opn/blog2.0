from django.urls import path, include

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView

from core.registries import plugin_registry, application_type_registry

from .user import urls as user_urls
from .user_files import urls as user_files_urls

app_name = "api"

urlpatterns = (
    [
        path("schema.json", SpectacularJSONAPIView.as_view(), name="json_schema"),
        path(
            "redoc/",
            SpectacularRedocView.as_view(url_name="api:json_schema"),
            name="redoc",
        ),
        path("user/", include(user_urls, namespace="user")),
        path("user-files/", include(user_files_urls, namespace="user_files")),
        path('user/', include('apps.user.urls', namespace="user_create")),
        # path('type/', include('apps.type.urls', namespace="types")),
        # path('repository/', include('apps.repository.urls', namespace="repository")),
        # path('lend/', include('apps.lend.urls', namespace="lend")),
        # path('employees/', include('apps.employees.urls', namespace="employees")),
        # path('manage/', include('apps.manage_asset.urls', namespace="manage")),

    ]
)
