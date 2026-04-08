from rest_framework.routers import DefaultRouter

from services.views import ServicesViewSet, SectorViewSet

router = DefaultRouter()
router.register(r"expertise-categories", ServicesViewSet, basename="expertisecategory")
router.register(r"sectors", SectorViewSet, basename="servicesector")

urlpatterns = router.urls
