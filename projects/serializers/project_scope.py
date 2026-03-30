from django_bolt.serializers import Serializer


class ProjectScopeSerializer(Serializer):
    id: int
    name: str
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "name", "order"],
            "detail": ["id", "name", "order"],
            "create": ["name", "order"],
            "update": ["name", "order"],
            "admin": ["id", "name", "order"],
        }


ProjectScopeListSerializer = ProjectScopeSerializer.fields("list")
ProjectScopeDetailSerializer = ProjectScopeSerializer.fields("detail")
ProjectScopeCreateSerializer = ProjectScopeSerializer.fields("create")
ProjectScopeUpdateSerializer = ProjectScopeSerializer.fields("update")
