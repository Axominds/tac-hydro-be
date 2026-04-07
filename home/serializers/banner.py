from load_env import env
from rest_framework import serializers

from home.models import Banner


class BannerListSerializer(serializers.ModelSerializer):
    background_image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ["id", "headline", "subheadline", "background_image", "typewriter_words"]

    def get_background_image(self, obj):
        if not obj.background_image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/background_image/"


class BannerDetailSerializer(BannerListSerializer):
    class Meta(BannerListSerializer.Meta):
        fields = ["id", "headline", "subheadline", "background_image", "typewriter_words"]


class BannerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["headline", "subheadline", "typewriter_words"]


class BannerUpdateSerializer(BannerCreateSerializer):
    class Meta(BannerCreateSerializer.Meta):
        pass
