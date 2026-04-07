from load_env import env
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
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/organization_chart_image/"


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
