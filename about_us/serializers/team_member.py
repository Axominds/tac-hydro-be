from load_env import env
from rest_framework import serializers

from about_us.models import TeamMember


class TeamMemberListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ["id", "name", "education", "bio", "is_active", "photo", "profile_photo"]

    def get_photo(self, obj):
        if not obj.photo:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/photo/"

    def get_profile_photo(self, obj):
        if not obj.profile_photo:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/profile_photo/"


class TeamMemberDetailSerializer(TeamMemberListSerializer):
    class Meta(TeamMemberListSerializer.Meta):
        pass


class TeamMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["name", "education", "bio", "is_active"]


class TeamMemberUpdateSerializer(TeamMemberCreateSerializer):
    class Meta(TeamMemberCreateSerializer.Meta):
        pass
