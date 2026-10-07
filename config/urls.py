from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogo.api_views import CancionViewSet, PlaylistViewSet

router = DefaultRouter()
router.register("canciones", CancionViewSet)
router.register("playlists", PlaylistViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalogo.urls")),
    path("api/", include(router.urls)),
    path("api-auth", include("rest_framework.urls")),
]