from django_bolt.views import ModelViewSet

from services.models import ServiceSector
from services.serializers.service_sector import (
    ServiceSectorDetailSerializer,
    ServiceSectorListSerializer,
)


class ServiceSectorViewSet(ModelViewSet):
    queryset = ServiceSector.objects.all()
    serializer_class = ServiceSectorDetailSerializer
    list_serializer_class = ServiceSectorListSerializer
