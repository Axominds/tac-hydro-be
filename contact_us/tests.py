from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient

from home.models import SiteSettings
from projects.models import ProjectScope
from contact_us.serializers.inquiry import (
    ContactInquirySerializer,
    CollaborationInquirySerializer,
)


class ContactInquirySerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            "name": "Jane Doe",
            "phone": "+977-9860080002",
            "email": "jane@example.com",
            "message": "Hello world",
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_nepal_and_standard_phone_formats(self):
        # Verify specific formats given by user
        phone_formats = [
            "01-4222832",
            "014222832",
            "9860080002",
            "+977-9860080002",
            "+9779860080002",
            "+1 (555) 019-2834",
            "123-456-7890",
        ]
        for phone in phone_formats:
            data = {
                "name": "John Doe",
                "phone": phone,
                "email": "john@example.com",
            }
            serializer = ContactInquirySerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Failed for phone format: {phone} - {serializer.errors}")

    def test_invalid_phone_format(self):
        data = {
            "name": "John Doe",
            "phone": "986abcd",  # contains letters
            "email": "john@example.com",
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_phone_too_short(self):
        data = {
            "name": "John Doe",
            "phone": "12345",  # too short (< 7 digits)
            "email": "john@example.com",
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_phone_too_long(self):
        data = {
            "name": "John Doe",
            "phone": "1" * 21,  # too long (> 20 digits)
            "email": "john@example.com",
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_invalid_name_format(self):
        data = {
            "name": "Jane123",  # contains digits
            "phone": "9860080002",
            "email": "jane@example.com",
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_too_short(self):
        data = {
            "name": "J",  # too short (< 2 characters)
            "phone": "9860080002",
            "email": "jane@example.com",
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_message_too_long(self):
        data = {
            "name": "Jane Doe",
            "phone": "9860080002",
            "email": "jane@example.com",
            "message": "a" * 5001,  # exceeds 5000 limit
        }
        serializer = ContactInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("message", serializer.errors)


class CollaborationInquirySerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "website": "https://example.com",
            "collab_type": "jv",
            "company_profile": "We build top tier hydropower plants since 2010.",
            "proposal_brief": "Let us collaborate on the next project.",
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_website(self):
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "website": "invalid-url",  # invalid URL format
            "company_profile": "We build top tier hydropower plants since 2010.",
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("website", serializer.errors)

    def test_invalid_collab_choices(self):
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "collab_type": "invalid_choice",  # not in choice list
            "company_profile": "We build top tier hydropower plants since 2010.",
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("collab_type", serializer.errors)

    def test_company_profile_too_short(self):
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "company_profile": "Short",  # less than 10 characters
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("company_profile", serializer.errors)

    def test_attachment_valid(self):
        # Create a mock text file that represents a small PDF
        pdf_file = SimpleUploadedFile("proposal.pdf", b"pdf_content", content_type="application/pdf")
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "company_profile": "We build top tier hydropower plants since 2010.",
            "attachment": pdf_file,
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_attachment_invalid_extension(self):
        # Create a mock png file, which is not allowed
        png_file = SimpleUploadedFile("photo.png", b"png_content", content_type="image/png")
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "company_profile": "We build top tier hydropower plants since 2010.",
            "attachment": png_file,
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("attachment", serializer.errors)

    def test_attachment_too_large(self):
        # Create a mock large file: 11MB
        large_content = b"0" * (11 * 1024 * 1024)
        pdf_file = SimpleUploadedFile("proposal.pdf", large_content, content_type="application/pdf")
        data = {
            "rep_name": "John Doe",
            "organization": "TAC Hydro Partner",
            "email": "partner@example.com",
            "phone": "9860080002",
            "company_profile": "We build top tier hydropower plants since 2010.",
            "attachment": pdf_file,
        }
        serializer = CollaborationInquirySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("attachment", serializer.errors)


class ContactInquiryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.settings = SiteSettings.objects.create(
            company_name="TAC Hydro",
            contact_email="contact@tachydro.com",
            collaboration_email="collab@tachydro.com"
        )
        self.url = reverse("contact-inquiry")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_success_post(self):
        data = {
            "name": "Jane Doe",
            "phone": "01-4222832",
            "email": "jane@example.com",
            "message": "Hi, I need help.",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Inquiry sent successfully")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_sent_on_success(self):
        data = {
            "name": "Jane Doe",
            "phone": "9860080002",
            "email": "jane@example.com",
            "message": "Hello from test",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "New Contact Inquiry from Jane Doe")
        self.assertEqual(email.to, ["contact@tachydro.com"])
        self.assertIn("Hello from test", email.body)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_sent_with_project_scope(self):
        scope = ProjectScope.objects.create(name="Test Project")
        data = {
            "name": "John Doe",
            "phone": "9860080002",
            "email": "john@example.com",
            "project_scope_id": scope.id,
            "message": "Interested in this project",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(f"Project Scope ID: {scope.id}", mail.outbox[0].body)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_not_sent_on_validation_error(self):
        data = {
            "name": "J",
            "phone": "invalid",
            "email": "bad-email",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_validation_error_returns_400(self):
        data = {
            "name": "J",
            "phone": "invalid",
            "email": "jane",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("phone", response.data)
        self.assertIn("email", response.data)

    def test_no_site_settings_returns_500(self):
        SiteSettings.objects.all().delete()
        data = {
            "name": "Jane Doe",
            "phone": "9860080002",
            "email": "jane@example.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)


class CollaborationInquiryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.settings = SiteSettings.objects.create(
            company_name="TAC Hydro",
            contact_email="contact@tachydro.com",
            collaboration_email="collab@tachydro.com"
        )
        self.url = reverse("collaboration-inquiry")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_success_post(self):
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Providing structural engineering since 2012.",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Collaboration inquiry sent successfully")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_sent_on_success(self):
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Providing structural engineering since 2012.",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "New Collaboration Inquiry from Jane Doe")
        self.assertEqual(email.to, ["collab@tachydro.com"])

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_with_attachment(self):
        pdf_file = SimpleUploadedFile("proposal.pdf", b"pdf_content", content_type="application/pdf")
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Providing structural engineering since 2012.",
            "attachment": pdf_file,
        }
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEqual(mail.outbox[0].attachments[0][0], "proposal.pdf")

    def test_attachment_invalid_extension_400(self):
        png_file = SimpleUploadedFile("photo.png", b"png_content", content_type="image/png")
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Providing structural engineering since 2012.",
            "attachment": png_file,
        }
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("attachment", response.data)

    def test_attachment_too_large_400(self):
        large_content = b"0" * (11 * 1024 * 1024)
        pdf_file = SimpleUploadedFile("proposal.pdf", large_content, content_type="application/pdf")
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Providing structural engineering since 2012.",
            "attachment": pdf_file,
        }
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("attachment", response.data)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_not_sent_on_validation_error(self):
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Short",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_no_site_settings_returns_500(self):
        SiteSettings.objects.all().delete()
        data = {
            "rep_name": "Jane Doe",
            "organization": "My Company",
            "phone": "9860080002",
            "email": "jane@example.com",
            "company_profile": "Providing structural engineering since 2012.",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
