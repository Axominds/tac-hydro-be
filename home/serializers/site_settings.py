import re
from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from home.models import SiteSettings

CURRENT_YEAR = date.today().year


def validate_file_size(value, max_mb=10):
    if hasattr(value, "size") and value.size > max_mb * 1024 * 1024:
        raise serializers.ValidationError(f"File size must not exceed {max_mb}MB")


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
        extra_kwargs = {
            "company_name": {
                "min_length": 1,
                "max_length": 255,
            },
            "tagline": {
                "max_length": 255,
            },
            "phone": {
                "max_length": 64,
            },
            "business_hours": {
                "max_length": 255,
            },
            "founded_year": {
                "min_value": 1800,
                "max_value": CURRENT_YEAR,
            },
        }

    def validate_phone(self, value):
        if value and not re.match(r"^[\d\s+\-()\.,]+$", value):
            raise serializers.ValidationError(
                "Enter a valid phone number (digits, spaces, +, -, (, ), ., and commas only)"
            )
        return value

    def validate_linkedin_url(self, value):
        if value and "linkedin.com" not in value.lower():
            raise serializers.ValidationError("Must be a valid LinkedIn URL containing linkedin.com")
        return value

    def validate_facebook_url(self, value):
        if value and "facebook.com" not in value.lower():
            raise serializers.ValidationError("Must be a valid Facebook URL containing facebook.com")
        return value

    def validate_organization_chart_image(self, value):
        validate_file_size(value)
        return value

    def validate_video(self, value):
        validate_file_size(value)
        return value

    def validate(self, data):
        video = data.get("video")
        youtube_url = data.get("youtube_url")
        if video and youtube_url:
            raise serializers.ValidationError("video and youtube_url are mutually exclusive")
        return data


class SiteSettingsUpdateSerializer(SiteSettingsCreateSerializer):
    class Meta(SiteSettingsCreateSerializer.Meta):
        pass
