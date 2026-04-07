from rest_framework import viewsets

from galleries.models import GallerySubcategory
from galleries.serializers.gallery_subcategory import (
    GallerySubcategoryCreateSerializer,
    GallerySubcategoryDetailSerializer,
    GallerySubcategoryListSerializer,
    GallerySubcategoryUpdateSerializer,
)


class GallerySubcategoryViewSet(viewsets.ModelViewSet):
    queryset = GallerySubcategory.objects.all()
    serializer_class = GallerySubcategoryDetailSerializer
    list_serializer_class = GallerySubcategoryListSerializer
    create_serializer_class = GallerySubcategoryCreateSerializer
    update_serializer_class = GallerySubcategoryUpdateSerializer
    partial_update_serializer_class = GallerySubcategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
