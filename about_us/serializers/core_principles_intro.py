from load_env import env
from rest_framework import serializers

from about_us.models import CorePrinciplesIntro


class CorePrinciplesIntroListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CorePrinciplesIntro
        fields = [
            "id",
            "title",
            "content_html",
            "image",
            "image_caption_title",
            "image_caption_subtitle",
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class CorePrinciplesIntroDetailSerializer(CorePrinciplesIntroListSerializer):
    class Meta(CorePrinciplesIntroListSerializer.Meta):
        pass


class CorePrinciplesIntroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorePrinciplesIntro
        fields = [
            "title",
            "content_html",
            "image_caption_title",
            "image_caption_subtitle",
        ]


class CorePrinciplesIntroUpdateSerializer(CorePrinciplesIntroCreateSerializer):
    class Meta(CorePrinciplesIntroCreateSerializer.Meta):
        pass
