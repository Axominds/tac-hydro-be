from rest_framework import serializers

from contact_us.models import PartnershipRoadmapStep


class PartnershipRoadmapStepListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipRoadmapStep
        fields = ["id", "section_id", "milestone", "title", "order"]


class PartnershipRoadmapStepDetailSerializer(PartnershipRoadmapStepListSerializer):
    class Meta(PartnershipRoadmapStepListSerializer.Meta):
        fields = [
            "id",
            "section_id",
            "milestone",
            "title",
            "description",
            "icon_key",
            "order",
        ]


class PartnershipRoadmapStepCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipRoadmapStep
        fields = [
            "section_id",
            "milestone",
            "title",
            "description",
            "icon_key",
            "order",
        ]


class PartnershipRoadmapStepUpdateSerializer(PartnershipRoadmapStepCreateSerializer):
    class Meta(PartnershipRoadmapStepCreateSerializer.Meta):
        pass
