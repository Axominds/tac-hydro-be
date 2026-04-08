from rest_framework import serializers

from galleries.models import GalleryCategory, GallerySubcategory


class GallerySubcategoryListSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)

    class Meta:
        model = GallerySubcategory
        fields = ["id", "category_id", "name", "order"]


class GallerySubcategoryDetailSerializer(GallerySubcategoryListSerializer):
    class Meta(GallerySubcategoryListSerializer.Meta):
        pass


class GallerySubcategoryCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=GalleryCategory.objects.all(), source="category"
    )

    class Meta:
        model = GallerySubcategory
        fields = ["category_id", "name", "order"]


class GallerySubcategoryUpdateSerializer(GallerySubcategoryCreateSerializer):
    class Meta(GallerySubcategoryCreateSerializer.Meta):
        pass
