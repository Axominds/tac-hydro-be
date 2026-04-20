from rest_framework.routers import DefaultRouter

from contact_us.views import (
    JobApplicationViewSet,
    JobCategoryViewSet,
    JobPostingViewSet,
)

router = DefaultRouter()
router.register(r"job-categories", JobCategoryViewSet, basename="jobcategory")
router.register(r"jobs", JobPostingViewSet, basename="jobposting")
router.register(r"job-applications", JobApplicationViewSet, basename="jobapplication")

urlpatterns = router.urls