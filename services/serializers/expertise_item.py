from rest_framework import serializers

from services.models import ExpertiseItem


class ExpertiseItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseItem
        fields = ["id", "category_id", "title", "project_scope_id", "order"]


class ExpertiseItemDetailSerializer(ExpertiseItemListSerializer):
    class Meta(ExpertiseItemListSerializer.Meta):
        pass


class ExpertiseItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseItem
        fields = ["category_id", "title", "project_scope_id", "order"]


class ExpertiseItemUpdateSerializer(ExpertiseItemCreateSerializer):
    class Meta(ExpertiseItemCreateSerializer.Meta):
        pass
