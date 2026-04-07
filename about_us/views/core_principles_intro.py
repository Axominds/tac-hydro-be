from rest_framework import viewsets

from about_us.models import CorePrinciplesIntro
from about_us.serializers.core_principles_intro import (
    CorePrinciplesIntroCreateSerializer,
    CorePrinciplesIntroDetailSerializer,
    CorePrinciplesIntroListSerializer,
    CorePrinciplesIntroUpdateSerializer,
)


class CorePrinciplesIntroViewSet(viewsets.ModelViewSet):
    queryset = CorePrinciplesIntro.objects.all()
    serializer_class = CorePrinciplesIntroDetailSerializer
    list_serializer_class = CorePrinciplesIntroListSerializer
    create_serializer_class = CorePrinciplesIntroCreateSerializer
    update_serializer_class = CorePrinciplesIntroUpdateSerializer
    partial_update_serializer_class = CorePrinciplesIntroUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
