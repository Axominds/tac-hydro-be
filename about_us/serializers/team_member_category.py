from django_bolt.serializers import Serializer


class TeamMemberCategorySerializer(Serializer):
    id: int
    team_member: int
    category: int
    position: str
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "team_member", "category", "position", "order"],
            "detail": ["id", "team_member", "category", "position", "order"],
            "create": ["team_member", "category", "position", "order"],
            "update": ["team_member", "category", "position", "order"],
            "admin": ["id", "team_member", "category", "position", "order"],
        }


TeamMemberCategoryListSerializer = TeamMemberCategorySerializer.fields("list")
TeamMemberCategoryDetailSerializer = TeamMemberCategorySerializer.fields("detail")
TeamMemberCategoryCreateSerializer = TeamMemberCategorySerializer.fields("create")
TeamMemberCategoryUpdateSerializer = TeamMemberCategorySerializer.fields("update")
