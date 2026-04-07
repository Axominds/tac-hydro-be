from rest_framework import serializers

from services.models import ExpertiseCategory


class ExpertiseCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseCategory
        fields = ["id", "title", "icon_key", "order", "theme_color"]


class ExpertiseCategoryDetailSerializer(ExpertiseCategoryListSerializer):
    class Meta(ExpertiseCategoryListSerializer.Meta):
        pass


class ExpertiseCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseCategory
        fields = ["title", "icon_key", "order", "theme_color"]


class ExpertiseCategoryUpdateSerializer(ExpertiseCategoryCreateSerializer):
    class Meta(ExpertiseCategoryCreateSerializer.Meta):
        pass
