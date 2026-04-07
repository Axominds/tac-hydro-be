from rest_framework import viewsets

from galleries.models import GalleryImage
from galleries.serializers.gallery_image import (
    GalleryImageCreateSerializer,
    GalleryImageDetailSerializer,
    GalleryImageListSerializer,
    GalleryImageUpdateSerializer,
)


class GalleryImageViewSet(viewsets.ModelViewSet):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageDetailSerializer
    list_serializer_class = GalleryImageListSerializer
    create_serializer_class = GalleryImageCreateSerializer
    update_serializer_class = GalleryImageUpdateSerializer
    partial_update_serializer_class = GalleryImageUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
