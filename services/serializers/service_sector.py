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
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


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
