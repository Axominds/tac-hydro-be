from rest_framework import viewsets

from projects.models import ProjectScope
from projects.serializers.project_scope import (
    ProjectScopeCreateSerializer,
    ProjectScopeDetailSerializer,
    ProjectScopeListSerializer,
    ProjectScopeUpdateSerializer,
)


class ProjectScopeViewSet(viewsets.ModelViewSet):
    queryset = ProjectScope.objects.all()
    serializer_class = ProjectScopeDetailSerializer
    list_serializer_class = ProjectScopeListSerializer
    create_serializer_class = ProjectScopeCreateSerializer
    update_serializer_class = ProjectScopeUpdateSerializer
    partial_update_serializer_class = ProjectScopeUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
