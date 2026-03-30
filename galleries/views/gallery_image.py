from django_bolt.views import ModelViewSet

from galleries.models import GalleryImage
from galleries.serializers.gallery_image import (
    GalleryImageDetailSerializer,
    GalleryImageListSerializer,
)


class GalleryImageViewSet(ModelViewSet):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageDetailSerializer
    list_serializer_class = GalleryImageListSerializer
