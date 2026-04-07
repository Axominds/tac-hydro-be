from load_env import env
from rest_framework import serializers

from home.models import ValuedPartner


class ValuedPartnerListSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = ValuedPartner
        fields = ["id", "name", "order", "logo"]

    def get_logo(self, obj):
        if not obj.logo:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/logo/"


class ValuedPartnerDetailSerializer(ValuedPartnerListSerializer):
    class Meta(ValuedPartnerListSerializer.Meta):
        pass


class ValuedPartnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValuedPartner
        fields = ["name", "order"]


class ValuedPartnerUpdateSerializer(ValuedPartnerCreateSerializer):
    class Meta(ValuedPartnerCreateSerializer.Meta):
        pass
