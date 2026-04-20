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
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class AboutPageSectionDetailSerializer(AboutPageSectionListSerializer):
    class Meta(AboutPageSectionListSerializer.Meta):
        pass


class AboutPageSectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPageSection
        fields = ["id", "section_key", "title", "content_html"]


class AboutPageSectionUpdateSerializer(AboutPageSectionCreateSerializer):
    class Meta(AboutPageSectionCreateSerializer.Meta):
        pass
