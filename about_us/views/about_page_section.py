from django_bolt.views import ModelViewSet

from about_us.models import AboutPageSection
from about_us.serializers.about_page_section import (
    AboutPageSectionDetailSerializer,
    AboutPageSectionListSerializer,
)


class AboutPageSectionViewSet(ModelViewSet):
    queryset = AboutPageSection.objects.all()
    serializer_class = AboutPageSectionDetailSerializer
    list_serializer_class = AboutPageSectionListSerializer
