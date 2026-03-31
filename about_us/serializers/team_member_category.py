from django_bolt.serializers import Serializer


class TeamMemberCategorySerializer(Serializer):
    id: int
    team_member_id: int
    category_id: int
    position: str
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "team_member_id", "category_id", "position", "order"],
            "detail": ["id", "team_member_id", "category_id", "position", "order"],
            "create": ["team_member_id", "category_id", "position", "order"],
            "update": ["team_member_id", "category_id", "position", "order"],
            "admin": ["id", "team_member_id", "category_id", "position", "order"],
        }


TeamMemberCategoryListSerializer = TeamMemberCategorySerializer.fields("list")
TeamMemberCategoryDetailSerializer = TeamMemberCategorySerializer.fields("detail")
TeamMemberCategoryCreateSerializer = TeamMemberCategorySerializer.fields("create")
TeamMemberCategoryUpdateSerializer = TeamMemberCategorySerializer.fields("update")
