from rest_framework import serializers


class ContactInquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=64, required=False, allow_blank=True)
    email = serializers.EmailField()
    project_scope_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField(required=False, allow_blank=True)


class CollaborationInquirySerializer(serializers.Serializer):
    rep_name = serializers.CharField(max_length=255)
    organization = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=64)
    website = serializers.URLField(required=False, allow_blank=True)
    collab_type = serializers.CharField(max_length=128, required=False, allow_blank=True)
    company_profile = serializers.CharField(required=False, allow_blank=True)
    proposal_brief = serializers.CharField(required=False, allow_blank=True)
    attachment = serializers.FileField(required=False, allow_null=True)
