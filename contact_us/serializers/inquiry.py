import re
import os
from rest_framework import serializers

def validate_name_field(value):
    if not value:
        return value
    if len(value) < 2:
        raise serializers.ValidationError("Name must be at least 2 characters long.")
    if len(value) > 100:
        raise serializers.ValidationError("Name cannot exceed 100 characters.")
    if not re.match(r"^[a-zA-Z\s'\-]+$", value):
        raise serializers.ValidationError("Name can only contain alphabetical characters, spaces, hyphens, and apostrophes.")
    return value

def validate_phone_field(value):
    if not value:
        return value
    if not re.match(r"^\+?[0-9\s\-\(\)]+$", value):
        raise serializers.ValidationError("Phone number can only contain digits, spaces, hyphens, parentheses, and start with +.")
    clean_digits = re.sub(r"\D", "", value)
    if len(clean_digits) < 7 or len(clean_digits) > 20:
        raise serializers.ValidationError("Phone number must contain between 7 and 20 digits.")
    return value

def validate_message_field(value):
    if not value:
        return value
    if len(value) > 5000:
        raise serializers.ValidationError("Message cannot exceed 5000 characters.")
    return value

def validate_organization_field(value):
    if not value:
        return value
    if len(value) < 2:
        raise serializers.ValidationError("Organization must be at least 2 characters long.")
    if len(value) > 200:
        raise serializers.ValidationError("Organization cannot exceed 200 characters.")
    return value

def validate_company_profile_field(value):
    if not value:
        return value
    if len(value) < 10:
        raise serializers.ValidationError("Company profile must be at least 10 characters long.")
    if len(value) > 5000:
        raise serializers.ValidationError("Company profile cannot exceed 5000 characters.")
    return value

def validate_proposal_brief_field(value):
    if not value:
        return value
    if len(value) > 1000:
        raise serializers.ValidationError("Proposal brief cannot exceed 1000 characters.")
    return value

def validate_attachment_field(file_obj):
    if file_obj:
        max_size = 10 * 1024 * 1024  # 10MB
        if file_obj.size > max_size:
            raise serializers.ValidationError("Attachment size cannot exceed 10MB.")
        
        allowed_extensions = ['.pdf', '.doc', '.docx']
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
    return file_obj


class ContactInquirySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, validators=[validate_name_field])
    phone = serializers.CharField(max_length=64, required=True, validators=[validate_phone_field])
    email = serializers.EmailField()
    project_scope_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField(required=False, allow_blank=True, validators=[validate_message_field])


class CollaborationInquirySerializer(serializers.Serializer):
    COLLAB_CHOICES = [
        ('jv', 'Strategic Joint Venture (JV)'),
        ('market', 'International Market Collaboration'),
        ('technical', 'Technical Expertise Partnerships'),
        ('research', 'Research Partnerships'),
        ('', 'Select Type'),
    ]

    rep_name = serializers.CharField(max_length=255, validators=[validate_name_field])
    organization = serializers.CharField(max_length=255, validators=[validate_organization_field])
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=64, validators=[validate_phone_field])
    website = serializers.URLField(required=False, allow_blank=True)
    collab_type = serializers.ChoiceField(choices=COLLAB_CHOICES, required=False, allow_blank=True)
    company_profile = serializers.CharField(required=False, allow_blank=True, validators=[validate_company_profile_field])
    proposal_brief = serializers.CharField(required=False, allow_blank=True, validators=[validate_proposal_brief_field])
    attachment = serializers.FileField(required=False, allow_null=True, validators=[validate_attachment_field])

