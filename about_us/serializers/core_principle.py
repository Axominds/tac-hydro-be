from rest_framework import serializers

from about_us.models import CorePrinciple


class CorePrincipleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorePrinciple
        fields = [
            "id",
            "title",
            "description",
            "icon_key",
            "color_class",
            "order",
        ]


class CorePrincipleDetailSerializer(CorePrincipleListSerializer):
    class Meta(CorePrincipleListSerializer.Meta):
        pass


class CorePrincipleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorePrinciple
        fields = ["title", "description", "icon_key", "color_class", "order"]


class CorePrincipleUpdateSerializer(CorePrincipleCreateSerializer):
    class Meta(CorePrincipleCreateSerializer.Meta):
        pass
