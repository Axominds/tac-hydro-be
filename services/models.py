from django.db import models


class ExpertiseCategory(models.Model):
    title = models.CharField(max_length=255)
    icon_key = models.CharField(max_length=64)
    order = models.PositiveIntegerField(default=0)
    theme_color = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "expertise_categories"
        ordering = ["order", "title"]

    def __str__(self) -> str:
        return self.title


class ExpertiseItem(models.Model):
    category = models.ForeignKey(ExpertiseCategory, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255)
    project_scope = models.ForeignKey(
        "projects.ProjectScope",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expertise_items",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "expertise_items"
        ordering = ["order", "title"]

    def __str__(self) -> str:
        return self.title


class ServiceSector(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="services/sectors", blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "service_sectors"
        ordering = ["order", "title"]

    def __str__(self) -> str:
        return self.title
