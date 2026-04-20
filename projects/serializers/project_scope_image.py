from rest_framework import serializers

from projects.models import ProjectScopeImage, ProjectScopeMembership


class ProjectScopeImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProjectScopeImage
        fields = ["id", "project_scope_membership_id", "alt_text", "order", "image"]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ProjectScopeImageDetailSerializer(ProjectScopeImageListSerializer):
    class Meta(ProjectScopeImageListSerializer.Meta):
        fields = ["id", "project_scope_membership_id", "alt_text", "order", "image"]


class ProjectScopeImageCreateSerializer(serializers.ModelSerializer):
    project_scope_membership_id = serializers.PrimaryKeyRelatedField(queryset=ProjectScopeMembership.objects.all(), source="project_scope_membership")
    class Meta:
        model = ProjectScopeImage
        fields = ["project_scope_membership_id", "alt_text", "order", "image"]


class ProjectScopeImageUpdateSerializer(ProjectScopeImageCreateSerializer):
    class Meta(ProjectScopeImageCreateSerializer.Meta):
        pass
