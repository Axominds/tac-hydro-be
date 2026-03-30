from django_bolt.serializers import Serializer


class NewsAttachmentSerializer(Serializer):
    id: int
    news: int
    file: str | None = None
    title: str | None = None

    class Config:
        field_sets = {
            "list": ["id", "news", "title"],
            "detail": ["id", "news", "title"],
            "create": ["news", "title"],
            "update": ["news", "title"],
            "admin": ["id", "news", "title"],
        }


NewsAttachmentListSerializer = NewsAttachmentSerializer.fields("list")
NewsAttachmentDetailSerializer = NewsAttachmentSerializer.fields("detail")
NewsAttachmentCreateSerializer = NewsAttachmentSerializer.fields("create")
NewsAttachmentUpdateSerializer = NewsAttachmentSerializer.fields("update")
