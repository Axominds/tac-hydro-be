from django_bolt.views import ModelViewSet

from about_us.models import TeamCategory
from about_us.serializers.team_category import (
    TeamCategoryDetailSerializer,
    TeamCategoryListSerializer,
)


class TeamCategoryViewSet(ModelViewSet):
    queryset = TeamCategory.objects.all()
    serializer_class = TeamCategoryDetailSerializer
    list_serializer_class = TeamCategoryListSerializer
