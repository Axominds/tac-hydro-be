from django_bolt.views import ModelViewSet

from services.models import ExpertiseItem
from services.serializers.expertise_item import (
    ExpertiseItemDetailSerializer,
    ExpertiseItemListSerializer,
)


class ExpertiseItemViewSet(ModelViewSet):
    queryset = ExpertiseItem.objects.all()
    serializer_class = ExpertiseItemDetailSerializer
    list_serializer_class = ExpertiseItemListSerializer
