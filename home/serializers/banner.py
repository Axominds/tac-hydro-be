from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from tac_hydro.extras import _serializer_instances
from load_env import env


class BannerSerializer(Serializer):
    id: int
    headline: str
    subheadline: str | None = None
    typewriter_words: list[str] | None = None

    @computed_field
    def background_image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/background_image/"

    class Config:
        field_sets = {
            "list": ["id", "headline", "subheadline", "background_image", "typewriter_words"],
            "detail": ["id", "headline", "subheadline", "background_image", "typewriter_words"],
            "create": ["headline", "subheadline", "typewriter_words"],
            "update": ["headline", "subheadline", "typewriter_words"],
            "admin": ["id", "headline", "subheadline", "typewriter_words"],
        }


BannerListSerializer = BannerSerializer.fields("list")
BannerDetailSerializer = BannerSerializer.fields("detail")
BannerCreateSerializer = BannerSerializer.fields("create")
BannerUpdateSerializer = BannerSerializer.fields("update")
