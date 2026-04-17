from load_env import env
from rest_framework import serializers

from projects.models import ProjectScopeImage


class ProjectScopeImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProjectScopeImage
        fields = ["id", "project_scope_membership_id", "alt_text", "order", "image"]

    def get_image(self, obj):
        if not obj.image:
            return None
        return f"{env.BACKEND_API_BASE_URL}/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/image/"


class ProjectScopeImageDetailSerializer(ProjectScopeImageListSerializer):
    class Meta(ProjectScopeImageListSerializer.Meta):
        fields = ["id", "project_scope_membership_id", "alt_text", "order", "image"]


class ProjectScopeImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScopeImage
        fields = ["project_scope_membership_id", "alt_text", "order", "image"]


class ProjectScopeImageUpdateSerializer(ProjectScopeImageCreateSerializer):
    class Meta(ProjectScopeImageCreateSerializer.Meta):
        pass
