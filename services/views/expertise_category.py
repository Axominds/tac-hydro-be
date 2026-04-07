from rest_framework import viewsets

from services.models import ExpertiseCategory
from services.serializers.expertise_category import (
    ExpertiseCategoryCreateSerializer,
    ExpertiseCategoryDetailSerializer,
    ExpertiseCategoryListSerializer,
    ExpertiseCategoryUpdateSerializer,
)


class ExpertiseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpertiseCategory.objects.all()
    serializer_class = ExpertiseCategoryDetailSerializer
    list_serializer_class = ExpertiseCategoryListSerializer
    create_serializer_class = ExpertiseCategoryCreateSerializer
    update_serializer_class = ExpertiseCategoryUpdateSerializer
    partial_update_serializer_class = ExpertiseCategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
