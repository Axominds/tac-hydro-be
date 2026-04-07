from rest_framework import serializers

from projects.models import ProjectScope


class ProjectScopeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScope
        fields = ["id", "name", "order"]


class ProjectScopeDetailSerializer(ProjectScopeListSerializer):
    class Meta(ProjectScopeListSerializer.Meta):
        pass


class ProjectScopeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScope
        fields = ["name", "order"]


class ProjectScopeUpdateSerializer(ProjectScopeCreateSerializer):
    class Meta(ProjectScopeCreateSerializer.Meta):
        pass
