from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from home.models import Banner
from home.serializers.banner import (
    BannerCreateSerializer,
    BannerDetailSerializer,
    BannerListSerializer,
    BannerUpdateSerializer,
)


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerDetailSerializer
    list_serializer_class = BannerListSerializer
    create_serializer_class = BannerCreateSerializer
    update_serializer_class = BannerUpdateSerializer
    partial_update_serializer_class = BannerUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="background_image")
    def background_image(self, request, pk=None):
        instance = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        instance.background_image = file
        instance.save()
        return Response({"detail": "Image uploaded successfully"})
