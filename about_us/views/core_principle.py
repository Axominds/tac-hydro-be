from rest_framework import viewsets

from about_us.models import CorePrinciple
from about_us.serializers.core_principle import (
    CorePrincipleCreateSerializer,
    CorePrincipleDetailSerializer,
    CorePrincipleListSerializer,
    CorePrincipleUpdateSerializer,
)


class CorePrincipleViewSet(viewsets.ModelViewSet):
    queryset = CorePrinciple.objects.all()
    serializer_class = CorePrincipleDetailSerializer
    list_serializer_class = CorePrincipleListSerializer
    create_serializer_class = CorePrincipleCreateSerializer
    update_serializer_class = CorePrincipleUpdateSerializer
    partial_update_serializer_class = CorePrincipleUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
