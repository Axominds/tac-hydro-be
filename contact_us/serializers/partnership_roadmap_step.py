from django_bolt.serializers import Serializer


class PartnershipRoadmapStepSerializer(Serializer):
    id: int
    section: int
    milestone: str
    title: str
    description: str | None = None
    icon_key: str
    order: int = 0

    class Config:
        field_sets = {
            "list": ["id", "section", "milestone", "title", "order"],
            "detail": [
                "id",
                "section",
                "milestone",
                "title",
                "description",
                "icon_key",
                "order",
            ],
            "create": [
                "section",
                "milestone",
                "title",
                "description",
                "icon_key",
                "order",
            ],
            "update": [
                "section",
                "milestone",
                "title",
                "description",
                "icon_key",
                "order",
            ],
            "admin": [
                "id",
                "section",
                "milestone",
                "title",
                "description",
                "icon_key",
                "order",
            ],
        }


PartnershipRoadmapStepListSerializer = PartnershipRoadmapStepSerializer.fields("list")
PartnershipRoadmapStepDetailSerializer = PartnershipRoadmapStepSerializer.fields("detail")
PartnershipRoadmapStepCreateSerializer = PartnershipRoadmapStepSerializer.fields("create")
PartnershipRoadmapStepUpdateSerializer = PartnershipRoadmapStepSerializer.fields("update")
