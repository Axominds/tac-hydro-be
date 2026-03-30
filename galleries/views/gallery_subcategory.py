from django_bolt.views import ModelViewSet

from galleries.models import GallerySubcategory
from galleries.serializers.gallery_subcategory import (
    GallerySubcategoryDetailSerializer,
    GallerySubcategoryListSerializer,
)


class GallerySubcategoryViewSet(ModelViewSet):
    queryset = GallerySubcategory.objects.all()
    serializer_class = GallerySubcategoryDetailSerializer
    list_serializer_class = GallerySubcategoryListSerializer
