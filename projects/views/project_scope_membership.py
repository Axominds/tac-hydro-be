from rest_framework import viewsets

from projects.models import ProjectScopeMembership
from projects.serializers.project_scope_membership import (
    ProjectScopeMembershipCreateSerializer,
    ProjectScopeMembershipDetailSerializer,
    ProjectScopeMembershipListSerializer,
    ProjectScopeMembershipUpdateSerializer,
)


class ProjectScopeMembershipViewSet(viewsets.ModelViewSet):
    queryset = ProjectScopeMembership.objects.prefetch_related("images").all()
    serializer_class = ProjectScopeMembershipDetailSerializer
    list_serializer_class = ProjectScopeMembershipListSerializer
    create_serializer_class = ProjectScopeMembershipCreateSerializer
    update_serializer_class = ProjectScopeMembershipUpdateSerializer
    partial_update_serializer_class = ProjectScopeMembershipUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
