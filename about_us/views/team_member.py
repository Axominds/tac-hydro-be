from django_bolt.views import ModelViewSet

from about_us.models import TeamMember
from about_us.serializers.team_member import (
    TeamMemberDetailSerializer,
    TeamMemberListSerializer,
)


class TeamMemberViewSet(ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberDetailSerializer
    list_serializer_class = TeamMemberListSerializer
