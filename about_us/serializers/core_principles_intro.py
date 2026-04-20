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
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


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
