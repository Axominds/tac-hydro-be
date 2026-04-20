"""
URL configuration for tac_hydro project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from home.urls import router as home_router
from home.views.stats import StatsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/home/", include(home_router.urls)),
    path("api/about-us/", include("about_us.urls")),
    path("api/services/", include("services.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/galleries/", include("galleries.urls")),
    path("api/contact-us/", include("contact_us.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/home/stats/", StatsView.as_view(), name="stats"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
