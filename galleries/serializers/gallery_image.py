from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from tac_hydro.extras import _serializer_instances
from load_env import env

class GalleryImageSerializer(Serializer):
    id: int
    gallery_subcategory_id: int
    image_path: str | None = None
    order: int = 0

    @computed_field
    def image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/image/"

    class Config:
        field_sets = {
            "list": ["id", "gallery_subcategory_id", "order", "image"],
            "detail": ["id", "gallery_subcategory_id", "order", "image"],
            "create": ["gallery_subcategory_id", "order"],
            "update": ["gallery_subcategory_id", "order"],
            "admin": ["id", "gallery_subcategory_id", "order", "image_path"],
        }


GalleryImageListSerializer = GalleryImageSerializer.fields("list")
GalleryImageDetailSerializer = GalleryImageSerializer.fields("detail")
GalleryImageCreateSerializer = GalleryImageSerializer.fields("create")
GalleryImageUpdateSerializer = GalleryImageSerializer.fields("update")
