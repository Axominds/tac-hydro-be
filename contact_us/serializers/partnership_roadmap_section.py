from django_bolt.serializers import Serializer


class PartnershipRoadmapSectionSerializer(Serializer):
    id: int
    title: str
    subtitle: str | None = None

    class Config:
        field_sets = {
            "list": ["id", "title"],
            "detail": ["id", "title", "subtitle"],
            "create": ["title", "subtitle"],
            "update": ["title", "subtitle"],
            "admin": ["id", "title", "subtitle"],
        }


PartnershipRoadmapSectionListSerializer = PartnershipRoadmapSectionSerializer.fields("list")
PartnershipRoadmapSectionDetailSerializer = PartnershipRoadmapSectionSerializer.fields("detail")
PartnershipRoadmapSectionCreateSerializer = PartnershipRoadmapSectionSerializer.fields("create")
PartnershipRoadmapSectionUpdateSerializer = PartnershipRoadmapSectionSerializer.fields("update")
