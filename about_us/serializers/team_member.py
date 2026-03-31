from load_env import env
from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from tac_hydro.extras import _serializer_instances


class TeamMemberSerializer(Serializer):
    id: int
    name: str
    education: str | None = None
    bio: str | None = None
    is_active: bool = True

    @computed_field
    def photo(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/photo/"

    class Config:
        field_sets = {
            "list": ["id", "name", "education", "bio", "is_active", "photo"],
            "detail": ["id", "name", "education", "bio", "is_active", "photo"],
            "create": ["name", "education", "bio", "is_active"],
            "update": ["name", "education", "bio", "is_active"],
            "admin": ["id", "name", "education", "bio", "is_active"],
        }


TeamMemberListSerializer = TeamMemberSerializer.fields("list")
TeamMemberDetailSerializer = TeamMemberSerializer.fields("detail")
TeamMemberCreateSerializer = TeamMemberSerializer.fields("create")
TeamMemberUpdateSerializer = TeamMemberSerializer.fields("update")
