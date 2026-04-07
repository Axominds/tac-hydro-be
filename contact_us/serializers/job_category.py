from rest_framework import serializers

from contact_us.models import JobCategory


class JobCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ["id", "name", "order"]


class JobCategoryDetailSerializer(JobCategoryListSerializer):
    class Meta(JobCategoryListSerializer.Meta):
        pass


class JobCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ["name", "order"]


class JobCategoryUpdateSerializer(JobCategoryCreateSerializer):
    class Meta(JobCategoryCreateSerializer.Meta):
        pass
