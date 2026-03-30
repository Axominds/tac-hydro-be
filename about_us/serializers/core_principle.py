from django_bolt.serializers import Serializer


class CorePrincipleSerializer(Serializer):
    id: int
    title: str
    description: str | None = None
    icon_key: str
    color_class: str
    order: int = 0

    class Config:
        field_sets = {
            "list": [
                "id",
                "title",
                "description",
                "icon_key",
                "color_class",
                "order",
            ],
            "detail": [
                "id",
                "title",
                "description",
                "icon_key",
                "color_class",
                "order",
            ],
            "create": ["title", "description", "icon_key", "color_class", "order"],
            "update": ["title", "description", "icon_key", "color_class", "order"],
            "admin": ["id", "title", "description", "icon_key", "color_class", "order"],
        }


CorePrincipleListSerializer = CorePrincipleSerializer.fields("list")
CorePrincipleDetailSerializer = CorePrincipleSerializer.fields("detail")
CorePrincipleCreateSerializer = CorePrincipleSerializer.fields("create")
CorePrincipleUpdateSerializer = CorePrincipleSerializer.fields("update")
