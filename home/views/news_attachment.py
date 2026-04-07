from rest_framework import viewsets

from home.models import NewsAttachment
from home.serializers.news_attachment import (
    NewsAttachmentCreateSerializer,
    NewsAttachmentDetailSerializer,
    NewsAttachmentListSerializer,
    NewsAttachmentUpdateSerializer,
)


class NewsAttachmentViewSet(viewsets.ModelViewSet):
    queryset = NewsAttachment.objects.all()
    serializer_class = NewsAttachmentDetailSerializer
    list_serializer_class = NewsAttachmentListSerializer
    create_serializer_class = NewsAttachmentCreateSerializer
    update_serializer_class = NewsAttachmentUpdateSerializer
    partial_update_serializer_class = NewsAttachmentUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
