from django_bolt.views import ModelViewSet

from home.models import SiteSettings
from home.serializers.site_settings import (
    SiteSettingsDetailSerializer,
    SiteSettingsListSerializer,
)


class SiteSettingsViewSet(ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsDetailSerializer
    list_serializer_class = SiteSettingsListSerializer
