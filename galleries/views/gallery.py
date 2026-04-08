from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.request import Request

from galleries.models import GalleryCategory, GallerySubcategory, GalleryImage
from galleries.serializers.gallery_category import (
    GalleryCategoryCreateSerializer,
    GalleryCategoryDetailSerializer,
    GalleryCategoryListSerializer,
    GalleryCategoryUpdateSerializer,
)
from galleries.serializers.gallery_subcategory import (
    GallerySubcategoryCreateSerializer,
    GallerySubcategoryDetailSerializer,
    GallerySubcategoryListSerializer,
    GallerySubcategoryUpdateSerializer,
)
from galleries.serializers.gallery_image import (
    GalleryImageCreateSerializer,
    GalleryImageDetailSerializer,
    GalleryImageListSerializer,
    GalleryImageUpdateSerializer,
)


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategoryDetailSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return GalleryCategoryListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return GalleryCategoryCreateSerializer
        return super().get_serializer_class()

    @action(detail=True, url_path="images")
    def category_images(self, request, pk=None):
        category = self.get_object()
        images = GalleryImage.objects.filter(gallery_subcategory__category=category)
        serializer = GalleryImageListSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="all-images")
    def all_images(self, request):
        images = GalleryImage.objects.all()
        serializer = GalleryImageListSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path="subcategories")
    def subcategories(self, request, pk=None):
        category = self.get_object()
        if request.method == "GET":
            subcategories = category.subcategories.all()
            serializer = GallerySubcategoryListSerializer(subcategories, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = GallerySubcategoryCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(category=category)
            return Response(
                GallerySubcategoryDetailSerializer(serializer.instance).data, status=status.HTTP_201_CREATED
            )

    @action(detail=True, url_path="subcategories/(?P<subcategory_id>[^/.]+)", methods=["get", "put", "patch", "delete"])
    def subcategory_detail(self, request: Request, pk=None, subcategory_id=None):
        category = self.get_object()
        try:
            subcategory = category.subcategories.get(pk=subcategory_id)
        except GallerySubcategory.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = GallerySubcategoryDetailSerializer(subcategory)
            return Response(serializer.data)
        elif request.method in ["PUT", "PATCH"]:
            serializer = GallerySubcategoryUpdateSerializer(
                subcategory, data=request.data, partial=request.method == "PATCH"
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(GallerySubcategoryDetailSerializer(subcategory).data)
        else:
            subcategory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        url_path="subcategories/(?P<subcategory_id>[^/.]+)/images",
        methods=["get", "post"],
        parser_classes=[MultiPartParser, FormParser, JSONParser],
    )
    def images(self, request: Request, pk=None, subcategory_id=None):
        category = self.get_object()
        try:
            subcategory = category.subcategories.get(pk=subcategory_id)
        except GallerySubcategory.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            images = subcategory.images.all()
            serializer = GalleryImageListSerializer(images, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = GalleryImageCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(gallery_subcategory=subcategory)
            return Response(GalleryImageDetailSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        url_path="subcategories/(?P<subcategory_id>[^/.]+)/images/(?P<image_id>[^/.]+)",
        methods=["get", "put", "patch", "delete"],
        parser_classes=[MultiPartParser, FormParser, JSONParser],
    )
    def image_detail(self, request: Request, pk=None, subcategory_id=None, image_id=None):
        category = self.get_object()
        try:
            subcategory = category.subcategories.get(pk=subcategory_id)
        except GallerySubcategory.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            image = subcategory.images.get(pk=image_id)
        except GalleryImage.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = GalleryImageDetailSerializer(image)
            return Response(serializer.data)
        elif request.method in ["PUT", "PATCH"]:
            serializer = GalleryImageUpdateSerializer(image, data=request.data, partial=request.method == "PATCH")
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(GalleryImageDetailSerializer(image).data)
        else:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
