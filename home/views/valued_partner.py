from rest_framework import viewsets

from home.models import ValuedPartner
from home.serializers.valued_partner import (
    ValuedPartnerCreateSerializer,
    ValuedPartnerDetailSerializer,
    ValuedPartnerListSerializer,
    ValuedPartnerUpdateSerializer,
)


class ValuedPartnerViewSet(viewsets.ModelViewSet):
    queryset = ValuedPartner.objects.all()
    serializer_class = ValuedPartnerDetailSerializer
    list_serializer_class = ValuedPartnerListSerializer
    create_serializer_class = ValuedPartnerCreateSerializer
    update_serializer_class = ValuedPartnerUpdateSerializer
    partial_update_serializer_class = ValuedPartnerUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
