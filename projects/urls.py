from django.urls import path
from rest_framework.routers import BaseRouter

from projects.views import (
    ProjectScopeImageViewSet,
    ProjectScopeMembershipViewSet,
    ProjectScopeViewSet,
    ProjectViewSet,
)


class ProjectRouter(BaseRouter):
    def get_urls(self):
        urls = [
            path("scopes/", self._register(ProjectScopeViewSet, "projectscope")),
            path("scopes/<int:pk>/", self._register_detail(ProjectScopeViewSet, "projectscope")),
            path("scope-memberships/", self._register(ProjectScopeMembershipViewSet, "projectscopemembership")),
            path(
                "scope-memberships/<int:pk>/",
                self._register_detail(ProjectScopeMembershipViewSet, "projectscopemembership"),
            ),
            path("scope-images/", self._register(ProjectScopeImageViewSet, "projectscopeimage")),
            path("scope-images/<int:pk>/", self._register_detail(ProjectScopeImageViewSet, "projectscopeimage")),
            path("", ProjectViewSet.as_view({"get": "list", "post": "create"}), name="project-list"),
            path(
                "<int:pk>/",
                ProjectViewSet.as_view(
                    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
                ),
                name="project-detail",
            ),
        ]
        return urls

    def _register(self, viewset, basename):
        return viewset.as_view({"get": "list", "post": "create"})

    def _register_detail(self, viewset, basename):
        return viewset.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"})


router = ProjectRouter()
urlpatterns = router.get_urls()