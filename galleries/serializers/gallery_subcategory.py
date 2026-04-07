from rest_framework import serializers

from galleries.models import GallerySubcategory


class GallerySubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GallerySubcategory
        fields = ["id", "category_id", "name", "order"]


class GallerySubcategoryDetailSerializer(GallerySubcategoryListSerializer):
    class Meta(GallerySubcategoryListSerializer.Meta):
        pass


class GallerySubcategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GallerySubcategory
        fields = ["category_id", "name", "order"]


class GallerySubcategoryUpdateSerializer(GallerySubcategoryCreateSerializer):
    class Meta(GallerySubcategoryCreateSerializer.Meta):
        pass
