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
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.logo.url)
        return obj.logo.url


class ValuedPartnerDetailSerializer(ValuedPartnerListSerializer):
    class Meta(ValuedPartnerListSerializer.Meta):
        pass


class ValuedPartnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValuedPartner
        fields = ["name", "order", "logo"]

    def create(self, validated_data):
        logo = validated_data.pop("logo", None)
        instance = super().create(validated_data)
        if logo:
            instance.logo = logo
            instance.save()
        return instance


class ValuedPartnerUpdateSerializer(ValuedPartnerCreateSerializer):
    class Meta:
        model = ValuedPartner
        fields = ["name", "order", "logo"]

    def update(self, instance, validated_data):
        logo = validated_data.pop("logo", None)
        instance = super().update(instance, validated_data)
        if logo:
            instance.logo = logo
            instance.save()
        return instance
