from rest_framework import viewsets

from projects.models import Project
from projects.serializers.project import (
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectUpdateSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    list_serializer_class = ProjectListSerializer
    create_serializer_class = ProjectCreateSerializer
    update_serializer_class = ProjectUpdateSerializer
    partial_update_serializer_class = ProjectUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
