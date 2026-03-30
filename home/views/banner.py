from django_bolt.views import ModelViewSet

from home.models import Banner
from home.serializers.banner import (
    BannerDetailSerializer,
    BannerListSerializer,
)


class BannerViewSet(ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerDetailSerializer
    list_serializer_class = BannerListSerializer
