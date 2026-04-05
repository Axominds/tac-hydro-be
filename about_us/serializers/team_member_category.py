from django_bolt.serializers import Serializer


class TeamMemberCategorySerializer(Serializer):
    id: int
    team_member_id: int
    category_id: int
    technical_expertise: str
    role: str | None = None
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "team_member_id", "category_id", "technical_expertise", "role", "order"],
            "detail": ["id", "team_member_id", "category_id", "technical_expertise", "role", "order"],
            "create": ["team_member_id", "category_id", "technical_expertise", "role", "order"],
            "update": ["team_member_id", "category_id", "technical_expertise", "role", "order"],
            "admin": ["id", "team_member_id", "category_id", "technical_expertise", "role", "order"],
        }


TeamMemberCategoryListSerializer = TeamMemberCategorySerializer.fields("list")
TeamMemberCategoryDetailSerializer = TeamMemberCategorySerializer.fields("detail")
TeamMemberCategoryCreateSerializer = TeamMemberCategorySerializer.fields("create")
TeamMemberCategoryUpdateSerializer = TeamMemberCategorySerializer.fields("update")
