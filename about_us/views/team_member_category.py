from rest_framework import viewsets

from about_us.models import TeamMemberCategory
from about_us.serializers.team_member_category import (
    TeamMemberCategoryCreateSerializer,
    TeamMemberCategoryDetailSerializer,
    TeamMemberCategoryListSerializer,
    TeamMemberCategoryUpdateSerializer,
)


class TeamMemberCategoryViewSet(viewsets.ModelViewSet):
    queryset = TeamMemberCategory.objects.select_related("team_member", "category")
    serializer_class = TeamMemberCategoryDetailSerializer
    list_serializer_class = TeamMemberCategoryListSerializer
    create_serializer_class = TeamMemberCategoryCreateSerializer
    update_serializer_class = TeamMemberCategoryUpdateSerializer
    partial_update_serializer_class = TeamMemberCategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
