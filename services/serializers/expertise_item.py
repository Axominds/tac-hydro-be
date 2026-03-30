from django_bolt.serializers import Serializer


class ExpertiseItemSerializer(Serializer):
    id: int
    category_id: int
    title: str
    project_scope_id: int | None = None
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "category_id", "title", "project_scope_id", "order"],
            "detail": ["id", "category_id", "title", "project_scope_id", "order"],
            "create": ["category_id", "title", "project_scope_id", "order"],
            "update": ["category_id", "title", "project_scope_id", "order"],
            "admin": ["id", "category_id", "title", "project_scope_id", "order"],
        }


ExpertiseItemListSerializer = ExpertiseItemSerializer.fields("list")
ExpertiseItemDetailSerializer = ExpertiseItemSerializer.fields("detail")
ExpertiseItemCreateSerializer = ExpertiseItemSerializer.fields("create")
ExpertiseItemUpdateSerializer = ExpertiseItemSerializer.fields("update")
