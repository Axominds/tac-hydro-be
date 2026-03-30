from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class ValuedPartnerSerializer(Serializer):
    id: int
    name: str
    logo_path: str | None = None
    order: int = 0

    @computed_field
    def logo(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/logo/"

    class Config:
        field_sets = {
            "list": ["id", "name", "order", "logo"],
            "detail": ["id", "name", "order", "logo"],
            "create": ["name", "order"],
            "update": ["name", "order"],
            "admin": ["id", "name", "order", "logo_path"],
        }


ValuedPartnerListSerializer = ValuedPartnerSerializer.fields("list")
ValuedPartnerDetailSerializer = ValuedPartnerSerializer.fields("detail")
ValuedPartnerCreateSerializer = ValuedPartnerSerializer.fields("create")
ValuedPartnerUpdateSerializer = ValuedPartnerSerializer.fields("update")
