from rest_framework import serializers

from about_us.models import TeamCategory


class TeamCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        fields = ["id", "name", "order"]


class TeamCategoryDetailSerializer(TeamCategoryListSerializer):
    class Meta(TeamCategoryListSerializer.Meta):
        pass


class TeamCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        fields = ["name", "order"]


class TeamCategoryUpdateSerializer(TeamCategoryCreateSerializer):
    class Meta(TeamCategoryCreateSerializer.Meta):
        pass
