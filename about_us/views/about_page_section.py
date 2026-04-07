from rest_framework import viewsets

from about_us.models import AboutPageSection
from about_us.serializers.about_page_section import (
    AboutPageSectionCreateSerializer,
    AboutPageSectionDetailSerializer,
    AboutPageSectionListSerializer,
    AboutPageSectionUpdateSerializer,
)


class AboutPageSectionViewSet(viewsets.ModelViewSet):
    queryset = AboutPageSection.objects.all()
    serializer_class = AboutPageSectionDetailSerializer
    list_serializer_class = AboutPageSectionListSerializer
    create_serializer_class = AboutPageSectionCreateSerializer
    update_serializer_class = AboutPageSectionUpdateSerializer
    partial_update_serializer_class = AboutPageSectionUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
