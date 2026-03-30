from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class ProjectScopeImageSerializer(Serializer):
    id: int
    project_scope_membership: int
    image_path: str | None = None
    alt_text: str | None = None
    order: int = 0

    @computed_field
    def image(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/image/"

    class Config:
        field_sets = {
            "list": ["id", "project_scope_membership", "alt_text", "order", "image"],
            "detail": ["id", "project_scope_membership", "alt_text", "order", "image"],
            "create": ["project_scope_membership", "alt_text", "order"],
            "update": ["project_scope_membership", "alt_text", "order"],
            "admin": ["id", "project_scope_membership", "alt_text", "order", "image_path"],
        }


ProjectScopeImageListSerializer = ProjectScopeImageSerializer.fields("list")
ProjectScopeImageDetailSerializer = ProjectScopeImageSerializer.fields("detail")
ProjectScopeImageCreateSerializer = ProjectScopeImageSerializer.fields("create")
ProjectScopeImageUpdateSerializer = ProjectScopeImageSerializer.fields("update")
