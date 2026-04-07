from load_env import env
from rest_framework import serializers

from galleries.models import GalleryImage


class GalleryImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = ["id", "gallery_subcategory_id", "order", "image"]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class GalleryImageDetailSerializer(GalleryImageListSerializer):
    class Meta(GalleryImageListSerializer.Meta):
        pass


class GalleryImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["gallery_subcategory_id", "order", "image"]


class GalleryImageUpdateSerializer(GalleryImageCreateSerializer):
    class Meta(GalleryImageCreateSerializer.Meta):
        pass
