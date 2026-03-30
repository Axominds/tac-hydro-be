from django_bolt.serializers import Serializer


class ProjectSerializer(Serializer):
    id: int
    title: str
    status: str | None = None
    installed_capacity: float
    installed_capacity_unit: str
    latitude: float
    longitude: float
    description: str | None = None
    technical_highlights: dict[str, str] | None = None

    class Config:
        field_sets = {
            "list": ["id", "title", "installed_capacity", "installed_capacity_unit", "latitude", "longitude"],
            "detail": [
                "id",
                "title",
                "status",
                "installed_capacity",
                "installed_capacity_unit",
                "latitude",
                "longitude",
                "description",
                "technical_highlights",
            ],
            "create": [
                "title",
                "status",
                "installed_capacity",
                "installed_capacity_unit",
                "latitude",
                "longitude",
                "description",
                "technical_highlights",
            ],
            "update": [
                "title",
                "status",
                "installed_capacity",
                "installed_capacity_unit",
                "latitude",
                "longitude",
                "description",
                "technical_highlights",
            ],
            "admin": [
                "id",
                "title",
                "status",
                "installed_capacity",
                "installed_capacity_unit",
                "latitude",
                "longitude",
                "description",
                "technical_highlights",
            ],
        }


ProjectListSerializer = ProjectSerializer.fields("list")
ProjectDetailSerializer = ProjectSerializer.fields("detail")
ProjectCreateSerializer = ProjectSerializer.fields("create")
ProjectUpdateSerializer = ProjectSerializer.fields("update")
