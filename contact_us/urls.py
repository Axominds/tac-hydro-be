from rest_framework.routers import DefaultRouter

from contact_us.views import (
    InitiateSynergySectionViewSet,
    JobApplicationViewSet,
    JobCategoryViewSet,
    JobPostingViewSet,
    PartnershipRoadmapSectionViewSet,
    PartnershipRoadmapStepViewSet,
)

router = DefaultRouter()
router.register(r"partnership-roadmap-sections", PartnershipRoadmapSectionViewSet, basename="partnershiproadmapsection")
router.register(r"partnership-roadmap-steps", PartnershipRoadmapStepViewSet, basename="partnershiproadmapstep")
router.register(r"initiate-synergy", InitiateSynergySectionViewSet, basename="initiatesynergysection")
router.register(r"job-categories", JobCategoryViewSet, basename="jobcategory")
router.register(r"jobs", JobPostingViewSet, basename="jobposting")
router.register(r"job-applications", JobApplicationViewSet, basename="jobapplication")

urlpatterns = router.urls
