from django_bolt.views import ModelViewSet

from home.models import ValuedPartner
from home.serializers.valued_partner import (
    ValuedPartnerDetailSerializer,
    ValuedPartnerListSerializer,
)


class ValuedPartnerViewSet(ModelViewSet):
    queryset = ValuedPartner.objects.all()
    serializer_class = ValuedPartnerDetailSerializer
    list_serializer_class = ValuedPartnerListSerializer
