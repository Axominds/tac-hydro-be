from rest_framework import serializers

from services.models import ExpertiseItem
from projects.models import ProjectScope


class ExpertiseItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseItem
        fields = ["id", "category_id", "title", "project_scope_id", "order"]


class ExpertiseItemDetailSerializer(ExpertiseItemListSerializer):
    class Meta(ExpertiseItemListSerializer.Meta):
        pass


class ExpertiseItemCreateSerializer(serializers.ModelSerializer):
    project_scope_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectScope.objects.all(),
        source="project_scope",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ExpertiseItem
        fields = ["category_id", "title", "project_scope_id", "order"]


class ExpertiseItemUpdateSerializer(ExpertiseItemCreateSerializer):
    class Meta(ExpertiseItemCreateSerializer.Meta):
        pass
