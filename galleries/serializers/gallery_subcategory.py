from django_bolt.serializers import Serializer


class GallerySubcategorySerializer(Serializer):
    id: int
    category_id: int
    name: str
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "category_id", "name", "order"],
            "detail": ["id", "category_id", "name", "order"],
            "create": ["category_id", "name", "order"],
            "update": ["category_id", "name", "order"],
            "admin": ["id", "category_id", "name", "order"],
        }


GallerySubcategoryListSerializer = GallerySubcategorySerializer.fields("list")
GallerySubcategoryDetailSerializer = GallerySubcategorySerializer.fields("detail")
GallerySubcategoryCreateSerializer = GallerySubcategorySerializer.fields("create")
GallerySubcategoryUpdateSerializer = GallerySubcategorySerializer.fields("update")
