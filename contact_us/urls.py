from django.urls import path

from contact_us.views.inquiry import ContactInquiryView, CollaborationInquiryView

urlpatterns = [
    path("inquiry/", ContactInquiryView.as_view(), name="contact-inquiry"),
    path("collaboration/", CollaborationInquiryView.as_view(), name="collaboration-inquiry"),
]