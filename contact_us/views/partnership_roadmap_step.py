from django_bolt.views import ModelViewSet

from contact_us.models import PartnershipRoadmapStep
from contact_us.serializers.partnership_roadmap_step import (
    PartnershipRoadmapStepDetailSerializer,
    PartnershipRoadmapStepListSerializer,
)


class PartnershipRoadmapStepViewSet(ModelViewSet):
    queryset = PartnershipRoadmapStep.objects.all()
    serializer_class = PartnershipRoadmapStepDetailSerializer
    list_serializer_class = PartnershipRoadmapStepListSerializer
