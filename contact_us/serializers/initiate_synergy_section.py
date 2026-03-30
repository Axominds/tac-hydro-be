from django_bolt.serializers import Serializer


class InitiateSynergySectionSerializer(Serializer):
    id: int
    title: str
    description: str | None = None
    cta_text: str | None = None
    cta_note: str | None = None

    class Config:
        field_sets = {
            "list": ["id", "title"],
            "detail": ["id", "title", "description", "cta_text", "cta_note"],
            "create": ["title", "description", "cta_text", "cta_note"],
            "update": ["title", "description", "cta_text", "cta_note"],
            "admin": ["id", "title", "description", "cta_text", "cta_note"],
        }


InitiateSynergySectionListSerializer = InitiateSynergySectionSerializer.fields("list")
InitiateSynergySectionDetailSerializer = InitiateSynergySectionSerializer.fields("detail")
InitiateSynergySectionCreateSerializer = InitiateSynergySectionSerializer.fields("create")
InitiateSynergySectionUpdateSerializer = InitiateSynergySectionSerializer.fields("update")
