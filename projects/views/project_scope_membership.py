from django_bolt.views import ModelViewSet

from projects.models import ProjectScopeMembership
from projects.serializers.project_scope_membership import (
    ProjectScopeMembershipDetailSerializer,
    ProjectScopeMembershipListSerializer,
)


class ProjectScopeMembershipViewSet(ModelViewSet):
    queryset = ProjectScopeMembership.objects.prefetch_related("images").all()
    serializer_class = ProjectScopeMembershipDetailSerializer
    list_serializer_class = ProjectScopeMembershipListSerializer
