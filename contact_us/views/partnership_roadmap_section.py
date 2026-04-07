from rest_framework import viewsets

from contact_us.models import PartnershipRoadmapSection
from contact_us.serializers.partnership_roadmap_section import (
    PartnershipRoadmapSectionCreateSerializer,
    PartnershipRoadmapSectionDetailSerializer,
    PartnershipRoadmapSectionListSerializer,
    PartnershipRoadmapSectionUpdateSerializer,
)


class PartnershipRoadmapSectionViewSet(viewsets.ModelViewSet):
    queryset = PartnershipRoadmapSection.objects.all()
    serializer_class = PartnershipRoadmapSectionDetailSerializer
    list_serializer_class = PartnershipRoadmapSectionListSerializer
    create_serializer_class = PartnershipRoadmapSectionCreateSerializer
    update_serializer_class = PartnershipRoadmapSectionUpdateSerializer
    partial_update_serializer_class = PartnershipRoadmapSectionUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
