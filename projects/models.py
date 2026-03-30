from django.core.exceptions import ValidationError
from django.db import models


class ProjectStatus(models.TextChoices):
    COMPLETED = "Completed", "Completed"
    ONGOING = "Ongoing", "Ongoing"


class ProjectScope(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "project_scopes"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=ProjectStatus.choices, blank=True)
    installed_capacity = models.FloatField()
    installed_capacity_unit = models.CharField(max_length=16, default="MW")
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    technical_highlights = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "projects"

    def __str__(self) -> str:
        return self.title


class ProjectScopeMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="scope_memberships")
    project_scope = models.ForeignKey(ProjectScope, on_delete=models.CASCADE, related_name="memberships")
    role = models.TextField(blank=True)

    class Meta:
        db_table = "project_scope_memberships"
        unique_together = ("project", "project_scope")

    def __str__(self) -> str:
        return f"{self.project} - {self.project_scope}"


class ProjectScopeImage(models.Model):
    project_scope_membership = models.ForeignKey(
        ProjectScopeMembership,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(upload_to="projects/scopes")
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "project_scope_images"
        ordering = ["order"]

    def clean(self) -> None:
        super().clean()
        if not self.project_scope_membership_id:
            return
        existing_count = ProjectScopeImage.objects.filter(
            project_scope_membership_id=self.project_scope_membership_id
        ).exclude(pk=self.pk)
        if existing_count.count() >= 4:
            raise ValidationError("A project scope can have at most 4 images.")

    def __str__(self) -> str:
        return f"{self.project_scope_membership} image {self.order}"
