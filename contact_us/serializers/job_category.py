from django_bolt.serializers import Serializer


class JobCategorySerializer(Serializer):
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


JobCategoryListSerializer = JobCategorySerializer.fields("list")
JobCategoryDetailSerializer = JobCategorySerializer.fields("detail")
JobCategoryCreateSerializer = JobCategorySerializer.fields("create")
JobCategoryUpdateSerializer = JobCategorySerializer.fields("update")
