from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class AboutPageSectionSerializer(Serializer):
    id: int
    section_key: str
    title: str
    content_html: str | None = None

    @computed_field
    def image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/image/"

    class Config:
        field_sets = {
            "list": ["id", "section_key", "title", "content_html", "image"],
            "detail": ["id", "section_key", "title", "content_html", "image"],
            "create": ["section_key", "title", "content_html"],
            "update": ["section_key", "title", "content_html"],
            "admin": ["id", "section_key", "title", "content_html"],
        }


AboutPageSectionListSerializer = AboutPageSectionSerializer.fields("list")
AboutPageSectionDetailSerializer = AboutPageSectionSerializer.fields("detail")
AboutPageSectionCreateSerializer = AboutPageSectionSerializer.fields("create")
AboutPageSectionUpdateSerializer = AboutPageSectionSerializer.fields("update")
