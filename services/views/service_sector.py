from rest_framework import viewsets

from services.models import ServiceSector
from services.serializers.service_sector import (
    ServiceSectorCreateSerializer,
    ServiceSectorDetailSerializer,
    ServiceSectorListSerializer,
    ServiceSectorUpdateSerializer,
)


class ServiceSectorViewSet(viewsets.ModelViewSet):
    queryset = ServiceSector.objects.all()
    serializer_class = ServiceSectorDetailSerializer
    list_serializer_class = ServiceSectorListSerializer
    create_serializer_class = ServiceSectorCreateSerializer
    update_serializer_class = ServiceSectorUpdateSerializer
    partial_update_serializer_class = ServiceSectorUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
