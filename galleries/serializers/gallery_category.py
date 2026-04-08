from rest_framework import serializers

from galleries.models import GalleryCategory, GallerySubcategory, GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    gallery_subcategory_id = serializers.IntegerField(source="gallery_subcategory.id", read_only=True)

    class Meta:
        model = GalleryImage
        fields = ["id", "gallery_subcategory_id", "order", "image"]

    def get_image(self, obj):
        from load_env import env

        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class GallerySubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GallerySubcategory
        fields = ["id", "category_id", "name", "order"]


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
