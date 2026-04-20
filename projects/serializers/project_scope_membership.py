from rest_framework import serializers

from projects.models import Project, ProjectScope, ProjectScopeImage, ProjectScopeMembership


class ProjectScopeMembershipListSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = ProjectScopeMembership
        fields = ["id", "project_id", "project_scope_id", "role", "image_urls"]

    def get_image_urls(self, obj):
        images = obj.images.all()
        request = self.context.get("request")
        urls = []
        for img in images:
            if img.image:
                if request:
                    urls.append(request.build_absolute_uri(img.image.url))
                else:
                    urls.append(img.image.url)
        return urls


class ProjectScopeMembershipDetailSerializer(ProjectScopeMembershipListSerializer):
    class Meta(ProjectScopeMembershipListSerializer.Meta):
        fields = ["id", "project_id", "project_scope_id", "role", "image_urls"]


class ProjectScopeMembershipCreateSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source="project"
    )
    project_scope_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectScope.objects.all(), source="project_scope"
    )

    class Meta:
        model = ProjectScopeMembership
        fields = ["project_id", "project_scope_id", "role"]


class ProjectScopeMembershipUpdateSerializer(ProjectScopeMembershipCreateSerializer):
    class Meta(ProjectScopeMembershipCreateSerializer.Meta):
        pass