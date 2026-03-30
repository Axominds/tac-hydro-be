from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class CorePrinciplesIntroSerializer(Serializer):
    id: int
    title: str
    content_html: str | None = None
    image_path: str | None = None
    image_caption_title: str | None = None
    image_caption_subtitle: str | None = None

    @computed_field
    def image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/image/"

    class Config:
        field_sets = {
            "list": [
                "id",
                "title",
                "content_html",
                "image",
                "image_caption_title",
                "image_caption_subtitle",
            ],
            "detail": [
                "id",
                "title",
                "content_html",
                "image",
                "image_caption_title",
                "image_caption_subtitle",
            ],
            "create": [
                "title",
                "content_html",
                "image_caption_title",
                "image_caption_subtitle",
            ],
            "update": [
                "title",
                "content_html",
                "image_caption_title",
                "image_caption_subtitle",
            ],
            "admin": [
                "id",
                "title",
                "content_html",
                "image_path",
                "image_caption_title",
                "image_caption_subtitle",
            ],
        }


CorePrinciplesIntroListSerializer = CorePrinciplesIntroSerializer.fields("list")
CorePrinciplesIntroDetailSerializer = CorePrinciplesIntroSerializer.fields("detail")
CorePrinciplesIntroCreateSerializer = CorePrinciplesIntroSerializer.fields("create")
CorePrinciplesIntroUpdateSerializer = CorePrinciplesIntroSerializer.fields("update")
