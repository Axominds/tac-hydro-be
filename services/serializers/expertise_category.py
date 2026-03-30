from django_bolt.serializers import Serializer


class ExpertiseCategorySerializer(Serializer):
    id: int
    title: str
    icon_key: str
    order: int = 0
    theme_color: str | None = None

    class Config:
        field_sets = {
            "list": ["id", "title", "icon_key", "order", "theme_color"],
            "detail": ["id", "title", "icon_key", "order", "theme_color"],
            "create": ["title", "icon_key", "order", "theme_color"],
            "update": ["title", "icon_key", "order", "theme_color"],
            "admin": ["id", "title", "icon_key", "order", "theme_color"],
        }


ExpertiseCategoryListSerializer = ExpertiseCategorySerializer.fields("list")
ExpertiseCategoryDetailSerializer = ExpertiseCategorySerializer.fields("detail")
ExpertiseCategoryCreateSerializer = ExpertiseCategorySerializer.fields("create")
ExpertiseCategoryUpdateSerializer = ExpertiseCategorySerializer.fields("update")
