from django_bolt.views import ModelViewSet

from contact_us.models import InitiateSynergySection
from contact_us.serializers.initiate_synergy_section import (
    InitiateSynergySectionDetailSerializer,
    InitiateSynergySectionListSerializer,
)


class InitiateSynergySectionViewSet(ModelViewSet):
    queryset = InitiateSynergySection.objects.all()
    serializer_class = InitiateSynergySectionDetailSerializer
    list_serializer_class = InitiateSynergySectionListSerializer
