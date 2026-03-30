from django_bolt.views import ModelViewSet

from projects.models import ProjectScopeImage
from projects.serializers.project_scope_image import (
    ProjectScopeImageDetailSerializer,
    ProjectScopeImageListSerializer,
)


class ProjectScopeImageViewSet(ModelViewSet):
    queryset = ProjectScopeImage.objects.all()
    serializer_class = ProjectScopeImageDetailSerializer
    list_serializer_class = ProjectScopeImageListSerializer
