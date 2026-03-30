from django_bolt.serializers import Serializer


class TeamCategorySerializer(Serializer):
    id: int
    name: str
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "name", "order"],
            "detail": ["id", "name", "order"],
            "create": ["name", "order"],
            "update": ["name", "order"],
            "admin": ["id", "name", "order"],
        }


TeamCategoryListSerializer = TeamCategorySerializer.fields("list")
TeamCategoryDetailSerializer = TeamCategorySerializer.fields("detail")
TeamCategoryCreateSerializer = TeamCategorySerializer.fields("create")
TeamCategoryUpdateSerializer = TeamCategorySerializer.fields("update")
