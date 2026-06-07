from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from home.models import SiteSettings
from projects.models import ProjectScope
from contact_us.models import JobApplication, JobPosting
from contact_us.serializers.inquiry import (
    ContactInquirySerializer,
    CollaborationInquirySerializer,
)
from contact_us.serializers.job_application import (
    JobApplicationCreateSerializer,
    JobApplicationListSerializer,
    JobApplicationDetailSerializer,
    JobApplicationUpdateSerializer,
)
from users.models import User


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}


def create_authenticated_client():
    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpass123",
    )
    client = APIClient()
    tokens = get_tokens(user)
    client.credentials(**tokens)
    return client, user


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


def _valid_job_application_data(job, extra=None):
    data = {
        "job_id": job.id,
        "first_name": "Jane",
        "last_name": "Doe",
        "gender": "Female",
        "phone": "9860080002",
        "email": "jane@example.com",
        "degree": "B.E. Civil",
        "grade": "A",
        "year_completed": "2023",
        "specialization": "Hydropower",
        "college": "IOE Pulchowk",
        "experience_sector": "Hydropower",
        "years_experience": "2",
        "cv_file": SimpleUploadedFile("cv.pdf", b"cv content", content_type="application/pdf"),
        "cover_letter_file": SimpleUploadedFile("cover.pdf", b"cover content", content_type="application/pdf"),
    }
    if extra:
        data.update(extra)
    return data


def _valid_consultant_data(job):
    return _valid_job_application_data(job)


def _valid_fulltime_data(job):
    return _valid_job_application_data(job, {
        "abilities": "Team leadership",
        "software_proficiency": "AutoCAD, MS Project",
        "employment_status": "Employed",
        "joining_date": "2026-08-01",
        "expected_salary": "80000",
    })


# ─── Job Application Serializer Tests ───────────────────────────────

class JobApplicationCreateSerializerTests(TestCase):
    def setUp(self):
        self.consultant_job = JobPosting.objects.create(
            title="Consultant",
            type="Independent Consultant",
            is_open=True,
        )
        self.fulltime_job = JobPosting.objects.create(
            title="Engineer",
            type="Full Time",
            is_open=True,
        )

    def test_valid_consultant_submission(self):
        data = _valid_consultant_data(self.consultant_job)
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_fulltime_submission(self):
        data = _valid_fulltime_data(self.fulltime_job)
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_model_level_required_fields(self):
        # first_name and last_name are required at the model level (no blank=True)
        data = {"job_id": self.fulltime_job.id}
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)

    def test_empty_required_fields_rejected_by_validate(self):
        # Fields with blank=True trigger validate() (not field-level), so
        # first_name and last_name must be valid to reach validate()
        data = {"job_id": self.fulltime_job.id, "first_name": "Jane", "last_name": "Doe"}
        for field in ["gender", "phone", "email",
                       "degree", "grade", "year_completed", "specialization",
                       "college", "experience_sector", "years_experience"]:
            data[field] = ""
        data["cv_file"] = SimpleUploadedFile("cv.pdf", b"content", content_type="application/pdf")
        data["cover_letter_file"] = SimpleUploadedFile("cover.pdf", b"content", content_type="application/pdf")
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        for field in ["gender", "phone", "email",
                       "degree", "grade", "year_completed", "specialization",
                       "college", "experience_sector", "years_experience"]:
            self.assertIn(field, serializer.errors, f"{field} should be required")

    def test_conditional_fields_required_for_fulltime(self):
        data = _valid_job_application_data(self.fulltime_job)
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        for field in ["abilities", "software_proficiency", "employment_status",
                       "joining_date", "expected_salary"]:
            self.assertIn(field, serializer.errors, f"{field} should be required for Full Time")

    def test_conditional_fields_optional_for_consultant(self):
        data = _valid_consultant_data(self.consultant_job)
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_email_rejected(self):
        data = _valid_fulltime_data(self.fulltime_job)
        data["email"] = "not-an-email"
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_consultant_can_omit_joining_date(self):
        data = _valid_consultant_data(self.consultant_job)
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_fulltime_rejects_empty_joining_date(self):
        data = _valid_fulltime_data(self.fulltime_job)
        data["joining_date"] = ""
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("joining_date", serializer.errors)

    def test_job_id_required(self):
        data = _valid_fulltime_data(self.fulltime_job)
        del data["job_id"]
        serializer = JobApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("job_id", serializer.errors)


class JobApplicationListSerializerTests(TestCase):
    def test_returns_email_field(self):
        job = JobPosting.objects.create(title="Engineer")
        app = JobApplication.objects.create(
            job=job,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )
        serializer = JobApplicationListSerializer(app)
        self.assertIn("email", serializer.data)
        self.assertEqual(serializer.data["email"], "jane@example.com")

    def test_list_fields(self):
        job = JobPosting.objects.create(title="Engineer")
        app = JobApplication.objects.create(
            job=job,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )
        serializer = JobApplicationListSerializer(app)
        expected = {"id", "job_id", "first_name", "last_name", "email", "submitted_at"}
        self.assertEqual(set(serializer.data.keys()), expected)


class JobApplicationDetailSerializerTests(TestCase):
    def test_detail_returns_full_data(self):
        job = JobPosting.objects.create(title="Engineer")
        app = JobApplication.objects.create(
            job=job,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="9860080002",
            degree="B.E.",
            abilities="Team leadership",
        )
        serializer = JobApplicationDetailSerializer(app)
        self.assertIn("email", serializer.data)
        self.assertIn("phone", serializer.data)
        self.assertIn("degree", serializer.data)
        self.assertIn("abilities", serializer.data)
        self.assertIn("cv_file", serializer.data)
        self.assertIn("cover_letter_file", serializer.data)


class JobApplicationUpdateSerializerTests(TestCase):
    def setUp(self):
        self.consultant_job = JobPosting.objects.create(
            title="Consultant",
            type="Independent Consultant",
        )
        self.fulltime_job = JobPosting.objects.create(
            title="Engineer",
            type="Full Time",
        )
        self.consultant_app = JobApplication.objects.create(
            job=self.consultant_job,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )
        self.fulltime_app = JobApplication.objects.create(
            job=self.fulltime_job,
            first_name="John",
            last_name="Smith",
            email="john@example.com",
        )

    def test_partial_update_single_field(self):
        serializer = JobApplicationUpdateSerializer(
            instance=self.consultant_app,
            data={"first_name": "Janet"},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_empty_required_field_rejected_on_update(self):
        serializer = JobApplicationUpdateSerializer(
            instance=self.consultant_app,
            data={"first_name": ""},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_conditional_fields_validated_on_fulltime_update(self):
        # Full Time — should require conditional fields when present in payload
        serializer = JobApplicationUpdateSerializer(
            instance=self.fulltime_app,
            data={"abilities": ""},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("abilities", serializer.errors)

    def test_conditional_fields_not_validated_on_consultant_update(self):
        serializer = JobApplicationUpdateSerializer(
            instance=self.consultant_app,
            data={},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_empty_joining_date_accepted_for_consultant(self):
        serializer = JobApplicationUpdateSerializer(
            instance=self.consultant_app,
            data={"joining_date": ""},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsNone(serializer.validated_data.get("joining_date"))

    def test_empty_joining_date_rejected_for_fulltime(self):
        serializer = JobApplicationUpdateSerializer(
            instance=self.fulltime_app,
            data={"joining_date": ""},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("joining_date", serializer.errors)


class JobApplicationCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job = JobPosting.objects.create(
            title="Engineer",
            type="Full Time",
            is_open=True,
        )
        self.url = reverse("jobapplication-list")
        self.settings = SiteSettings.objects.create(
            contact_email="contact@tachydro.com",
        )

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_create_without_auth_success(self):
        data = _valid_fulltime_data(self.job)
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], "jane@example.com")

    def test_create_without_auth_validation_error(self):
        data = {"job_id": self.job.id}
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_sent_on_success(self):
        data = _valid_fulltime_data(self.job)
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn(self.job.title, email.subject)
        self.assertIn("jane@example.com", email.body)
        self.assertEqual(email.to, ["contact@tachydro.com"])

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_not_sent_on_validation_error(self):
        data = {"job_id": self.job.id, "first_name": ""}
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_email_with_consultant_submission(self):
        consultant_job = JobPosting.objects.create(
            title="Consultant",
            type="Independent Consultant",
            is_open=True,
        )
        data = _valid_consultant_data(consultant_job)
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

    def test_no_site_settings_still_saves(self):
        SiteSettings.objects.all().delete()
        data = _valid_fulltime_data(self.job)
        response = self.client.post(self.url, data, format="multipart")
        # Email failure is logged, but the application is still saved
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_cv_returns_400(self):
        data = _valid_fulltime_data(self.job)
        del data["cv_file"]
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cv_file", response.data)

    def test_missing_cover_letter_returns_400(self):
        data = _valid_fulltime_data(self.job)
        del data["cover_letter_file"]
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cover_letter_file", response.data)


class JobApplicationAdminViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.job = JobPosting.objects.create(title="Engineer", type="Full Time")
        self.application = JobApplication.objects.create(
            job=self.job,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )
        self.list_url = reverse("jobapplication-list")
        self.detail_url = reverse("jobapplication-detail", args=[self.application.id])

    def test_list_requires_auth(self):
        anonymous_client = APIClient()
        response = anonymous_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_applications(self):
        response = self.client.get(self.list_url, {"page": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_returns_email_field(self):
        response = self.client.get(self.list_url, {"page": 1})
        self.assertIn("email", response.data["results"][0])

    def test_list_filters_by_job_id(self):
        other_job = JobPosting.objects.create(title="Consultant", type="Independent Consultant")
        JobApplication.objects.create(job=other_job, first_name="John", last_name="Doe", email="john@example.com")
        response = self.client.get(self.list_url, {"page": 1, "job_id": self.job.id})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["email"], "jane@example.com")

    def test_list_filters_by_search(self):
        response = self.client.get(self.list_url, {"page": 1, "search": "Jane"})
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_search_by_email(self):
        response = self.client.get(self.list_url, {"page": 1, "search": "jane@example.com"})
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_search_no_match(self):
        response = self.client.get(self.list_url, {"page": 1, "search": "nonexistent"})
        self.assertEqual(len(response.data["results"]), 0)

    def test_list_pagination(self):
        for i in range(15):
            JobApplication.objects.create(
                job=self.job,
                first_name=f"User{i}",
                last_name="Test",
                email=f"user{i}@example.com",
            )
        response = self.client.get(self.list_url, {"page": 1, "page_size": 10})
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["count"], 16)

    def test_detail_requires_auth(self):
        anonymous_client = APIClient()
        response = anonymous_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_returns_full_data(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("email", response.data)
        self.assertIn("cv_file", response.data)

    def test_update_requires_auth(self):
        anonymous_client = APIClient()
        response = anonymous_client.patch(self.detail_url, {"first_name": "Janet"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_success(self):
        response = self.client.patch(self.detail_url, {"first_name": "Janet"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.first_name, "Janet")

    def test_update_rejects_empty_required_field(self):
        response = self.client.patch(self.detail_url, {"first_name": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)

    def test_full_update_rejects_empty_required(self):
        response = self.client.put(
            self.detail_url,
            {"first_name": "", "last_name": ""},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)

    def test_update_all_fields(self):
        response = self.client.put(
            self.detail_url,
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "gender": "Female",
                "phone": "9860080002",
                "email": "jane@example.com",
                "degree": "B.E.",
                "grade": "A",
                "year_completed": "2023",
                "specialization": "Hydropower",
                "college": "IOE",
                "experience_sector": "Hydropower",
                "years_experience": "3",
                "abilities": "Teamwork",
                "software_proficiency": "AutoCAD",
                "employment_status": "Employed",
                "joining_date": "2026-08-01",
                "expected_salary": "90000",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.years_experience, "3")
        self.assertEqual(self.application.expected_salary, "90000")

    def test_consultant_update_ignores_conditional_fields(self):
        consultant_job = JobPosting.objects.create(title="Consultant", type="Independent Consultant")
        app = JobApplication.objects.create(
            job=consultant_job,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
        )
        detail_url = reverse("jobapplication-detail", args=[app.id])
        response = self.client.patch(detail_url, {"first_name": "Johnny"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        app.refresh_from_db()
        self.assertEqual(app.first_name, "Johnny")

    def test_delete_removes_application(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobApplication.objects.filter(id=self.application.id).exists())
