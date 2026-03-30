from django.db import models


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=64, blank=True)
    contact_email = models.EmailField(blank=True)
    collaboration_email = models.EmailField(blank=True)
    business_hours = models.CharField(max_length=255, blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    map_embed_url = models.URLField(blank=True)
    organization_chart_image = models.FileField(upload_to="home/organization", blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "site_settings"

    def __str__(self) -> str:
        return self.company_name


class Banner(models.Model):
    headline = models.CharField(max_length=255)
    subheadline = models.TextField(blank=True)
    background_image = models.FileField(upload_to="home/banners")
    typewriter_words = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "banners"

    def __str__(self) -> str:
        return self.headline


class ValuedPartner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.FileField(upload_to="home/partners")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "valued_partners"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "news_categories"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    news_category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT, related_name="news")
    image = models.FileField(upload_to="home/news", blank=True)
    news_date = models.DateField()
    published_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "news"
        ordering = ["-news_date", "title"]

    def __str__(self) -> str:
        return self.title


class NewsAttachment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="home/news/attachments")
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "news_attachments"

    def __str__(self) -> str:
        return self.title or self.file.name
