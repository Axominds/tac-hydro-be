from rest_framework import serializers

from about_us.models import TeamMemberCategory


class TeamMemberCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = ["id", "team_member_id", "category_id", "technical_expertise", "role", "order"]


class TeamMemberCategoryDetailSerializer(TeamMemberCategoryListSerializer):
    class Meta(TeamMemberCategoryListSerializer.Meta):
        pass


class TeamMemberCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = ["team_member_id", "category_id", "technical_expertise", "role", "order"]


class TeamMemberCategoryUpdateSerializer(TeamMemberCategoryCreateSerializer):
    class Meta(TeamMemberCategoryCreateSerializer.Meta):
        pass
