from rest_framework import viewsets

from about_us.models import TeamMember
from about_us.serializers.team_member import (
    TeamMemberCreateSerializer,
    TeamMemberDetailSerializer,
    TeamMemberListSerializer,
    TeamMemberUpdateSerializer,
)


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberDetailSerializer
    list_serializer_class = TeamMemberListSerializer
    create_serializer_class = TeamMemberCreateSerializer
    update_serializer_class = TeamMemberUpdateSerializer
    partial_update_serializer_class = TeamMemberUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
