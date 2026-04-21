from django.urls import path
from rest_framework.routers import DefaultRouter

from contact_us.views import (
    JobApplicationViewSet,
    JobCategoryViewSet,
    JobPostingViewSet,
)
from contact_us.views.inquiry import ContactInquiryView, CollaborationInquiryView

router = DefaultRouter()
router.register(r"job-categories", JobCategoryViewSet, basename="jobcategory")
router.register(r"jobs", JobPostingViewSet, basename="jobposting")
router.register(r"job-applications", JobApplicationViewSet, basename="jobapplication")

urlpatterns = router.urls

urlpatterns += [
    path("inquiry/", ContactInquiryView.as_view(), name="contact-inquiry"),
    path("collaboration/", CollaborationInquiryView.as_view(), name="collaboration-inquiry"),
]