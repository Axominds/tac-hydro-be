from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from about_us.models import AboutPageSection
from about_us.serializers.about_page_section import (
    AboutPageSectionCreateSerializer,
    AboutPageSectionDetailSerializer,
    AboutPageSectionListSerializer,
    AboutPageSectionUpdateSerializer,
)


class AboutPageSectionViewSet(viewsets.ModelViewSet):
    queryset = AboutPageSection.objects.all()
    serializer_class = AboutPageSectionDetailSerializer
    list_serializer_class = AboutPageSectionListSerializer
    create_serializer_class = AboutPageSectionCreateSerializer
    update_serializer_class = AboutPageSectionUpdateSerializer
    partial_update_serializer_class = AboutPageSectionUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="image")
    def upload_image(self, request, pk=None):
        instance = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        instance.image = file
        instance.save()
        return Response({"detail": "Image uploaded successfully"})
