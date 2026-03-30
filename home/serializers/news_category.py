from django_bolt.serializers import Serializer


class NewsCategorySerializer(Serializer):
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


NewsCategoryListSerializer = NewsCategorySerializer.fields("list")
NewsCategoryDetailSerializer = NewsCategorySerializer.fields("detail")
NewsCategoryCreateSerializer = NewsCategorySerializer.fields("create")
NewsCategoryUpdateSerializer = NewsCategorySerializer.fields("update")
