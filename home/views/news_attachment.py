from django_bolt.views import ModelViewSet

from home.models import NewsAttachment
from home.serializers.news_attachment import (
    NewsAttachmentDetailSerializer,
    NewsAttachmentListSerializer,
)


class NewsAttachmentViewSet(ModelViewSet):
    queryset = NewsAttachment.objects.all()
    serializer_class = NewsAttachmentDetailSerializer
    list_serializer_class = NewsAttachmentListSerializer
