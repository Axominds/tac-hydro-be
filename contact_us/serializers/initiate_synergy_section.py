from rest_framework import serializers

from contact_us.models import InitiateSynergySection


class InitiateSynergySectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiateSynergySection
        fields = ["id", "title"]


class InitiateSynergySectionDetailSerializer(InitiateSynergySectionListSerializer):
    class Meta(InitiateSynergySectionListSerializer.Meta):
        fields = ["id", "title", "description", "cta_text", "cta_note"]


class InitiateSynergySectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiateSynergySection
        fields = ["title", "description", "cta_text", "cta_note"]


class InitiateSynergySectionUpdateSerializer(InitiateSynergySectionCreateSerializer):
    class Meta(InitiateSynergySectionCreateSerializer.Meta):
        pass
