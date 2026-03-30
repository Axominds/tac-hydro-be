from django_bolt.views import ModelViewSet

from services.models import ExpertiseCategory
from services.serializers.expertise_category import (
    ExpertiseCategoryDetailSerializer,
    ExpertiseCategoryListSerializer,
)


class ExpertiseCategoryViewSet(ModelViewSet):
    queryset = ExpertiseCategory.objects.all()
    serializer_class = ExpertiseCategoryDetailSerializer
    list_serializer_class = ExpertiseCategoryListSerializer
