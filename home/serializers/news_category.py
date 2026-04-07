from rest_framework import serializers

from home.models import NewsCategory


class NewsCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name", "order"]


class NewsCategoryDetailSerializer(NewsCategoryListSerializer):
    class Meta(NewsCategoryListSerializer.Meta):
        pass


class NewsCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["name", "order"]


class NewsCategoryUpdateSerializer(NewsCategoryCreateSerializer):
    class Meta(NewsCategoryCreateSerializer.Meta):
        pass
