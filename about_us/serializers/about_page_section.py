from load_env import env
from rest_framework import serializers

from about_us.models import AboutPageSection


class AboutPageSectionListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AboutPageSection
        fields = ["id", "section_key", "title", "content_html", "image"]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class AboutPageSectionDetailSerializer(AboutPageSectionListSerializer):
    class Meta(AboutPageSectionListSerializer.Meta):
        pass


class AboutPageSectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPageSection
        fields = ["section_key", "title", "content_html"]


class AboutPageSectionUpdateSerializer(AboutPageSectionCreateSerializer):
    class Meta(AboutPageSectionCreateSerializer.Meta):
        pass
