from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from home.models import SiteSettings
from home.serializers.site_settings import (
    SiteSettingsCreateSerializer,
    SiteSettingsDetailSerializer,
    SiteSettingsListSerializer,
    SiteSettingsUpdateSerializer,
)


class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsDetailSerializer
    list_serializer_class = SiteSettingsListSerializer
    create_serializer_class = SiteSettingsCreateSerializer
    update_serializer_class = SiteSettingsUpdateSerializer
    partial_update_serializer_class = SiteSettingsUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="organization_chart_image")
    def organization_chart_image(self, request, pk=None):
        instance = self.get_object()
        file = request.FILES.get("organization_chart_image")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        instance.organization_chart_image = file
        instance.save()
        return Response({"detail": "Image uploaded successfully"})
