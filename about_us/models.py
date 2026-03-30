from django.db import models


class AboutPageSection(models.Model):
    section_key = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255)
    content_html = models.TextField(blank=True)
    image = models.FileField(upload_to="about_us/sections", blank=True)

    class Meta:
        db_table = "about_page_sections"

    def __str__(self) -> str:
        return self.title


class CorePrinciplesIntro(models.Model):
    title = models.CharField(max_length=255)
    content_html = models.TextField(blank=True)
    image = models.FileField(upload_to="about_us/core_principles", blank=True)
    image_caption_title = models.CharField(max_length=255, blank=True)
    image_caption_subtitle = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "core_principles_intros"

    def __str__(self) -> str:
        return self.title


class CorePrinciple(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon_key = models.CharField(max_length=64)
    color_class = models.CharField(max_length=64)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "core_principles"
        ordering = ["order", "title"]

    def __str__(self) -> str:
        return self.title


class TeamCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "team_categories"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    education = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    photo = models.FileField(upload_to="about_us/team", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "team_members"

    def __str__(self) -> str:
        return self.name


class TeamMemberCategory(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name="categories")
    category = models.ForeignKey(TeamCategory, on_delete=models.CASCADE, related_name="team_members")
    position = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "team_member_categories"
        ordering = ["order", "position"]

    def __str__(self) -> str:
        return f"{self.team_member} - {self.category}"
