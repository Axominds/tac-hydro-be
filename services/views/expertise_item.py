from rest_framework import viewsets

from services.models import ExpertiseItem
from services.serializers.expertise_item import (
    ExpertiseItemCreateSerializer,
    ExpertiseItemDetailSerializer,
    ExpertiseItemListSerializer,
    ExpertiseItemUpdateSerializer,
)


class ExpertiseItemViewSet(viewsets.ModelViewSet):
    queryset = ExpertiseItem.objects.all()
    serializer_class = ExpertiseItemDetailSerializer
    list_serializer_class = ExpertiseItemListSerializer
    create_serializer_class = ExpertiseItemCreateSerializer
    update_serializer_class = ExpertiseItemUpdateSerializer
    partial_update_serializer_class = ExpertiseItemUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
