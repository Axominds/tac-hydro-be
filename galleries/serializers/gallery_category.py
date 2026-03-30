from django_bolt.serializers import Serializer


class GalleryCategorySerializer(Serializer):
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


GalleryCategoryListSerializer = GalleryCategorySerializer.fields("list")
GalleryCategoryDetailSerializer = GalleryCategorySerializer.fields("detail")
GalleryCategoryCreateSerializer = GalleryCategorySerializer.fields("create")
GalleryCategoryUpdateSerializer = GalleryCategorySerializer.fields("update")
