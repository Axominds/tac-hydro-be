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
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url

    def get_profile_photo(self, obj):
        if not obj.profile_photo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.profile_photo.url)
        return obj.profile_photo.url


class TeamMemberDetailSerializer(TeamMemberListSerializer):
    class Meta(TeamMemberListSerializer.Meta):
        pass


class TeamMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["name", "education", "bio", "is_active", "photo", "profile_photo"]


class TeamMemberUpdateSerializer(TeamMemberCreateSerializer):
    class Meta(TeamMemberCreateSerializer.Meta):
        pass
