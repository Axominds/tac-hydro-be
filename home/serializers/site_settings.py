from rest_framework import serializers

from home.models import SiteSettings


class SiteSettingsListSerializer(serializers.ModelSerializer):
    organization_chart_image = serializers.SerializerMethodField()

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
        ]

    def get_organization_chart_image(self, obj):
        if not obj.organization_chart_image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.organization_chart_image.url)
        return obj.organization_chart_image.url


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
        ]


class SiteSettingsUpdateSerializer(SiteSettingsCreateSerializer):
    class Meta(SiteSettingsCreateSerializer.Meta):
        pass
