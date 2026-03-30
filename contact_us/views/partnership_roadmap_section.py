from django_bolt.views import ModelViewSet

from contact_us.models import PartnershipRoadmapSection
from contact_us.serializers.partnership_roadmap_section import (
    PartnershipRoadmapSectionDetailSerializer,
    PartnershipRoadmapSectionListSerializer,
)


class PartnershipRoadmapSectionViewSet(ModelViewSet):
    queryset = PartnershipRoadmapSection.objects.all()
    serializer_class = PartnershipRoadmapSectionDetailSerializer
    list_serializer_class = PartnershipRoadmapSectionListSerializer
