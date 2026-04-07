from rest_framework.routers import DefaultRouter

from galleries.views import (
    GalleryCategoryViewSet,
    GalleryImageViewSet,
    GallerySubcategoryViewSet,
)

router = DefaultRouter()
router.register(r"categories", GalleryCategoryViewSet, basename="gallerycategory")
router.register(r"subcategories", GallerySubcategoryViewSet, basename="gallerysubcategory")
router.register(r"images", GalleryImageViewSet, basename="galleryimage")

urlpatterns = router.urls
