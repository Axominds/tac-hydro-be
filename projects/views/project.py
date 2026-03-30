from django_bolt.views import ModelViewSet

from projects.models import Project
from projects.serializers.project import (
    ProjectDetailSerializer,
    ProjectListSerializer,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    list_serializer_class = ProjectListSerializer

    # retrieve API at the moment required explicit override in django-bolt
    async def retrieve(self, request, pk):
        return await super().retrieve(request, pk=pk)
