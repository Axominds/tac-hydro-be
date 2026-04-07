from rest_framework.routers import DefaultRouter

from services.views import (
    ExpertiseCategoryViewSet,
    ExpertiseItemViewSet,
    ServiceSectorViewSet,
)

router = DefaultRouter()
router.register(r"expertise-categories", ExpertiseCategoryViewSet, basename="expertisecategory")
router.register(r"expertise-items", ExpertiseItemViewSet, basename="expertiseitem")
router.register(r"sectors", ServiceSectorViewSet, basename="servicesector")

urlpatterns = router.urls
