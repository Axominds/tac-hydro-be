from rest_framework import serializers

from home.models import SiteSettings


class SiteSettingsListSerializer(serializers.ModelSerializer):
    organization_chart_image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            "id",
            "company_name",
            "tagline",
            "address",
            "phone",
            "contact_email",
            "collaboration_email",
            "business_hours",
            "facebook_url",
            "linkedin_url",
            "map_embed_url",
            "organization_chart_image",
            "founded_year",
            "video",
            "youtube_url",
        ]

    def get_organization_chart_image(self, obj):
        if not obj.organization_chart_image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.organization_chart_image.url)
        return obj.organization_chart_image.url

    def get_video(self, obj):
        if not obj.video:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url


class SiteSettingsDetailSerializer(SiteSettingsListSerializer):
    class Meta(SiteSettingsListSerializer.Meta):
        pass


class SiteSettingsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "company_name",
            "tagline",
            "address",
            "phone",
            "contact_email",
            "collaboration_email",
            "business_hours",
            "facebook_url",
            "linkedin_url",
            "map_embed_url",
            "organization_chart_image",
            "founded_year",
            "video",
            "youtube_url",
        ]

    def validate(self, data):
        video = data.get("video")
        youtube_url = data.get("youtube_url")
        if video and youtube_url:
            raise serializers.ValidationError("video and youtube_url are mutually exclusive")
        return data


class SiteSettingsUpdateSerializer(SiteSettingsCreateSerializer):
    class Meta(SiteSettingsCreateSerializer.Meta):
        pass
