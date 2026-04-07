from rest_framework import viewsets

from galleries.models import GalleryCategory
from galleries.serializers.gallery_category import (
    GalleryCategoryCreateSerializer,
    GalleryCategoryDetailSerializer,
    GalleryCategoryListSerializer,
    GalleryCategoryUpdateSerializer,
)


class GalleryCategoryViewSet(viewsets.ModelViewSet):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategoryDetailSerializer
    list_serializer_class = GalleryCategoryListSerializer
    create_serializer_class = GalleryCategoryCreateSerializer
    update_serializer_class = GalleryCategoryUpdateSerializer
    partial_update_serializer_class = GalleryCategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
