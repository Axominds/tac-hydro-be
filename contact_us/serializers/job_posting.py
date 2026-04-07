from rest_framework import serializers

from contact_us.models import JobPosting


class JobPostingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ["id", "title", "category_id", "type", "is_open"]


class JobPostingDetailSerializer(JobPostingListSerializer):
    class Meta(JobPostingListSerializer.Meta):
        fields = [
            "id",
            "title",
            "category_id",
            "type",
            "location",
            "description",
            "responsibilities",
            "qualifications",
            "is_open",
            "published_at",
        ]


class JobPostingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            "title",
            "category_id",
            "type",
            "location",
            "description",
            "responsibilities",
            "qualifications",
            "is_open",
            "published_at",
        ]


class JobPostingUpdateSerializer(JobPostingCreateSerializer):
    class Meta(JobPostingCreateSerializer.Meta):
        pass
