from load_env import env
from rest_framework import serializers

from services.models import ServiceSector


class ServiceSectorListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ServiceSector
        fields = ["id", "title", "description", "order", "image"]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class ServiceSectorDetailSerializer(ServiceSectorListSerializer):
    class Meta(ServiceSectorListSerializer.Meta):
        pass


class ServiceSectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSector
        fields = ["title", "description", "order", "image"]


class ServiceSectorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSector
        fields = ["title", "description", "order", "image"]
