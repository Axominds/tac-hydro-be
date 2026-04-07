from load_env import env
from rest_framework import serializers

from contact_us.models import JobApplication


class JobApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "job_id", "first_name", "last_name", "status"]


class JobApplicationDetailSerializer(JobApplicationListSerializer):
    cv_file = serializers.SerializerMethodField()
    cover_letter_file = serializers.SerializerMethodField()

    class Meta(JobApplicationListSerializer.Meta):
        fields = [
            "id",
            "job_id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "phone",
            "email",
            "degree",
            "grade",
            "year_completed",
            "specialization",
            "college",
            "abilities",
            "software_proficiency",
            "employment_status",
            "experience_sector",
            "years_experience",
            "joining_date",
            "expected_salary",
            "cv_file",
            "cover_letter_file",
            "submitted_at",
            "status",
        ]

    def get_cv_file(self, obj):
        if not obj.cv_file:
            return None
        return f"/api/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/cv_file"

    def get_cover_letter_file(self, obj):
        if not obj.cover_letter_file:
            return None
        return f"/api/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/cover_letter_file"


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "job_id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "phone",
            "email",
            "degree",
            "grade",
            "year_completed",
            "specialization",
            "college",
            "abilities",
            "software_proficiency",
            "employment_status",
            "experience_sector",
            "years_experience",
            "joining_date",
            "expected_salary",
            "status",
        ]


class JobApplicationUpdateSerializer(JobApplicationCreateSerializer):
    class Meta(JobApplicationCreateSerializer.Meta):
        pass
