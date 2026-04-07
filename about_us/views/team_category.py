from rest_framework import viewsets

from about_us.models import TeamCategory
from about_us.serializers.team_category import (
    TeamCategoryCreateSerializer,
    TeamCategoryDetailSerializer,
    TeamCategoryListSerializer,
    TeamCategoryUpdateSerializer,
)


class TeamCategoryViewSet(viewsets.ModelViewSet):
    queryset = TeamCategory.objects.all()
    serializer_class = TeamCategoryDetailSerializer
    list_serializer_class = TeamCategoryListSerializer
    create_serializer_class = TeamCategoryCreateSerializer
    update_serializer_class = TeamCategoryUpdateSerializer
    partial_update_serializer_class = TeamCategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
