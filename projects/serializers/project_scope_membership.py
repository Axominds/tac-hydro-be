from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from load_env import env
from tac_hydro.extras import _serializer_instances


class ProjectScopeMembershipSerializer(Serializer):
    id: int
    project_id: int
    project_scope_id: int
    role: str | None = None
    images: list[int] | None = None

    @computed_field
    def image_urls(self) -> list[str]:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return []
        return [
            f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/projectscopeimage/{img_pk}/image/"
            for img_pk in self.images
        ]

    class Config:
        field_sets = {
            "list": ["id", "project_id", "project_scope_id", "role", "image_urls", "images"],
            "detail": ["id", "project_id", "project_scope_id", "role", "image_urls", "images"],
            "create": ["project_id", "project_scope_id", "role"],
            "update": ["project_id", "project_scope_id", "role"],
            "admin": ["id", "project_id", "project_scope_id", "role", "image_urls", "images"],
        }


ProjectScopeMembershipListSerializer = ProjectScopeMembershipSerializer.fields("list")
ProjectScopeMembershipDetailSerializer = ProjectScopeMembershipSerializer.fields("detail")
ProjectScopeMembershipCreateSerializer = ProjectScopeMembershipSerializer.fields("create")
ProjectScopeMembershipUpdateSerializer = ProjectScopeMembershipSerializer.fields("update")
