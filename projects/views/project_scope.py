from django_bolt.views import ModelViewSet

from projects.models import ProjectScope
from projects.serializers.project_scope import (
    ProjectScopeDetailSerializer,
    ProjectScopeListSerializer,
)


class ProjectScopeViewSet(ModelViewSet):
    queryset = ProjectScope.objects.all()
    serializer_class = ProjectScopeDetailSerializer
    list_serializer_class = ProjectScopeListSerializer
