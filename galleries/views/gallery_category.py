from django_bolt.views import ModelViewSet

from galleries.models import GalleryCategory
from galleries.serializers.gallery_category import (
    GalleryCategoryDetailSerializer,
    GalleryCategoryListSerializer,
)


class GalleryCategoryViewSet(ModelViewSet):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategoryDetailSerializer
    list_serializer_class = GalleryCategoryListSerializer
