from rest_framework import serializers

from galleries.models import GalleryCategory


class GalleryCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ["id", "name", "order"]


class GalleryCategoryDetailSerializer(GalleryCategoryListSerializer):
    class Meta(GalleryCategoryListSerializer.Meta):
        pass


class GalleryCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ["name", "order"]


class GalleryCategoryUpdateSerializer(GalleryCategoryCreateSerializer):
    class Meta(GalleryCategoryCreateSerializer.Meta):
        pass
