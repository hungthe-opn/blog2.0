from django.urls import path, include
from django.contrib import admin

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView

from core.registries import plugin_registry, application_type_registry
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
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
        path("blog/", include('apps.blog_it.urls', namespace="blog_it")),
        path("category/", include('apps.categorys.urls', namespace="category")),
        path("post-empl/", include('apps.empl.urls', namespace="admin-blog")),
        path('auth/', include('rest_framework.urls', namespace='rest_framework')),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path("comment/", include('apps.comment.urls', namespace="comment")),
        # path("contact/", include('apps.contact.urls', namespace="contact")),
        path("forum/", include('apps.forum.urls', namespace="forum")),
        path("user-blog/", include('apps.user.urls', namespace="user")),

    ]
)
