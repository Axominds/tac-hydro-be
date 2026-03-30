from django_bolt.views import ModelViewSet

from about_us.models import TeamMemberCategory
from about_us.serializers.team_member_category import (
    TeamMemberCategoryDetailSerializer,
    TeamMemberCategoryListSerializer,
)


class TeamMemberCategoryViewSet(ModelViewSet):
    queryset = TeamMemberCategory.objects.all()
    serializer_class = TeamMemberCategoryDetailSerializer
    list_serializer_class = TeamMemberCategoryListSerializer
