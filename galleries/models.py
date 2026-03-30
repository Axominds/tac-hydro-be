from django.db import models


class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "gallery_categories"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class GallerySubcategory(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "gallery_subcategories"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class GalleryImage(models.Model):
    gallery_subcategory = models.ForeignKey(
        GallerySubcategory,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.FileField(upload_to="galleries/images")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "gallery_images"
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.gallery_subcategory} image {self.order}"
