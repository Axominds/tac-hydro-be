from rest_framework import serializers

from projects.models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "installed_capacity", "installed_capacity_unit", "latitude", "longitude"]


class ProjectDetailSerializer(ProjectListSerializer):
    class Meta(ProjectListSerializer.Meta):
        fields = [
            "id",
            "title",
            "status",
            "installed_capacity",
            "installed_capacity_unit",
            "latitude",
            "longitude",
            "description",
            "technical_highlights",
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "title",
            "status",
            "installed_capacity",
            "installed_capacity_unit",
            "latitude",
            "longitude",
            "description",
            "technical_highlights",
        ]


class ProjectUpdateSerializer(ProjectCreateSerializer):
    class Meta(ProjectCreateSerializer.Meta):
        pass
