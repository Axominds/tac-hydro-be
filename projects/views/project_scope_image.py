from rest_framework import viewsets

from projects.models import ProjectScopeImage
from projects.serializers.project_scope_image import (
    ProjectScopeImageCreateSerializer,
    ProjectScopeImageDetailSerializer,
    ProjectScopeImageListSerializer,
    ProjectScopeImageUpdateSerializer,
)


class ProjectScopeImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectScopeImage.objects.all()
    serializer_class = ProjectScopeImageDetailSerializer
    list_serializer_class = ProjectScopeImageListSerializer
    create_serializer_class = ProjectScopeImageCreateSerializer
    update_serializer_class = ProjectScopeImageUpdateSerializer
    partial_update_serializer_class = ProjectScopeImageUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
