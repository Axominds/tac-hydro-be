from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class ServiceSectorSerializer(Serializer):
    id: int
    title: str
    image_path: str | None = None
    description: str | None = None
    order: int = 0

    @computed_field
    def image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/image/"

    class Config:
        field_sets = {
            "list": ["id", "title", "description", "order", "image"],
            "detail": ["id", "title", "description", "order", "image"],
            "create": ["title", "description", "order"],
            "update": ["title", "description", "order"],
            "admin": ["id", "title", "description", "order", "image_path"],
        }


ServiceSectorListSerializer = ServiceSectorSerializer.fields("list")
ServiceSectorDetailSerializer = ServiceSectorSerializer.fields("detail")
ServiceSectorCreateSerializer = ServiceSectorSerializer.fields("create")
ServiceSectorUpdateSerializer = ServiceSectorSerializer.fields("update")
