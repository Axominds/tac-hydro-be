from rest_framework import serializers

from contact_us.models import PartnershipRoadmapSection


class PartnershipRoadmapSectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipRoadmapSection
        fields = ["id", "title"]


class PartnershipRoadmapSectionDetailSerializer(PartnershipRoadmapSectionListSerializer):
    class Meta(PartnershipRoadmapSectionListSerializer.Meta):
        fields = ["id", "title", "subtitle"]


class PartnershipRoadmapSectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipRoadmapSection
        fields = ["title", "subtitle"]


class PartnershipRoadmapSectionUpdateSerializer(PartnershipRoadmapSectionCreateSerializer):
    class Meta(PartnershipRoadmapSectionCreateSerializer.Meta):
        pass
