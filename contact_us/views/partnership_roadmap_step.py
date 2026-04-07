from rest_framework import viewsets

from contact_us.models import PartnershipRoadmapStep
from contact_us.serializers.partnership_roadmap_step import (
    PartnershipRoadmapStepCreateSerializer,
    PartnershipRoadmapStepDetailSerializer,
    PartnershipRoadmapStepListSerializer,
    PartnershipRoadmapStepUpdateSerializer,
)


class PartnershipRoadmapStepViewSet(viewsets.ModelViewSet):
    queryset = PartnershipRoadmapStep.objects.all()
    serializer_class = PartnershipRoadmapStepDetailSerializer
    list_serializer_class = PartnershipRoadmapStepListSerializer
    create_serializer_class = PartnershipRoadmapStepCreateSerializer
    update_serializer_class = PartnershipRoadmapStepUpdateSerializer
    partial_update_serializer_class = PartnershipRoadmapStepUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
