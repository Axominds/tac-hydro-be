from rest_framework.routers import DefaultRouter

from galleries.views import GalleryViewSet

router = DefaultRouter()
router.register(r"categories", GalleryViewSet, basename="gallery")

urlpatterns = router.urls
