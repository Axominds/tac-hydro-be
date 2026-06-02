"""
URL configuration for tac_hydro project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from home.urls import router as home_router
from home.views.admin_stats import AdminDashboardStatsView
from home.views.stats import StatsView
from home.views.change_password import ChangePasswordView
from home.views.token import TokenValidateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/home/", include(home_router.urls)),
    path("api/about-us/", include("about_us.urls")),
    path("api/services/", include("services.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/galleries/", include("galleries.urls")),
    path("api/contact-us/", include("contact_us.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="token_obtain_pair"),
    path("api/auth/token-refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),
    path("api/auth/validate/", TokenValidateView.as_view(), name="token_validate"),
    path("api/auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("api/home/stats/", StatsView.as_view(), name="stats"),
    path("api/home/admin-stats/", AdminDashboardStatsView.as_view(), name="admin-stats"),
]

urlpatterns += [
    re_path(r"^api/media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
