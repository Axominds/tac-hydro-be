from rest_framework import viewsets

from contact_us.models import InitiateSynergySection
from contact_us.serializers.initiate_synergy_section import (
    InitiateSynergySectionCreateSerializer,
    InitiateSynergySectionDetailSerializer,
    InitiateSynergySectionListSerializer,
    InitiateSynergySectionUpdateSerializer,
)


class InitiateSynergySectionViewSet(viewsets.ModelViewSet):
    queryset = InitiateSynergySection.objects.all()
    serializer_class = InitiateSynergySectionDetailSerializer
    list_serializer_class = InitiateSynergySectionListSerializer
    create_serializer_class = InitiateSynergySectionCreateSerializer
    update_serializer_class = InitiateSynergySectionUpdateSerializer
    partial_update_serializer_class = InitiateSynergySectionUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
