from datetime import date
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from home.models import (
    Banner,
    News,
    NewsAttachment,
    NewsCategory,
    SiteSettings,
    ValuedPartner,
)
from home.serializers.banner import (
    BannerCreateSerializer,
    BannerDetailSerializer,
    BannerListSerializer,
    BannerUpdateSerializer,
)
from home.serializers.news import (
    NewsCreateSerializer,
    NewsListSerializer,
    NewsRetrieveSerializer,
    NewsUpdateSerializer,
)
from home.serializers.news_attachment import (
    NewsAttachmentCreateSerializer,
    NewsAttachmentDetailSerializer,
    NewsAttachmentListSerializer,
    NewsAttachmentUpdateSerializer,
)
from home.serializers.news_category import (
    NewsCategoryCreateSerializer,
    NewsCategoryDetailSerializer,
    NewsCategoryListSerializer,
    NewsCategoryUpdateSerializer,
)
from home.serializers.site_settings import (
    SiteSettingsCreateSerializer,
    SiteSettingsDetailSerializer,
    SiteSettingsListSerializer,
    SiteSettingsUpdateSerializer,
)
from home.serializers.valued_partner import (
    ValuedPartnerCreateSerializer,
    ValuedPartnerDetailSerializer,
    ValuedPartnerListSerializer,
    ValuedPartnerUpdateSerializer,
)
from about_us.models import TeamMember
from projects.models import Project, ProjectScope, ProjectScopeMembership
from services.models import ExpertiseCategory, ServiceSector
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


# ─── Model Tests ───────────────────────────────────────────────────

class SiteSettingsModelTests(TestCase):
    def test_create_site_settings(self):
        settings = SiteSettings.objects.create(
            company_name="TAC Hydro",
            tagline="Powering Nepal",
            contact_email="info@tachydro.com",
        )
        self.assertEqual(str(settings), "TAC Hydro")

    def test_video_and_youtube_mutually_exclusive(self):
        settings = SiteSettings(
            company_name="Test",
            video=SimpleUploadedFile("vid.mp4", b"content"),
            youtube_url="https://youtube.com/watch?v=123",
        )
        with self.assertRaises(ValidationError):
            settings.full_clean()


class BannerModelTests(TestCase):
    def test_create_banner(self):
        banner = Banner.objects.create(
            headline="Welcome",
            subheadline="To TAC Hydro",
            typewriter_words=["reliable", "efficient"],
        )
        self.assertEqual(str(banner), "Welcome")
        self.assertEqual(banner.typewriter_words, ["reliable", "efficient"])


class ValuedPartnerModelTests(TestCase):
    def test_create_partner(self):
        partner = ValuedPartner.objects.create(
            name="Partner A", order=1, logo=SimpleUploadedFile("logo.png", b"img")
        )
        self.assertEqual(str(partner), "Partner A")

    def test_default_ordering(self):
        ValuedPartner.objects.create(name="B", order=2, logo=SimpleUploadedFile("l.png", b"i"))
        ValuedPartner.objects.create(name="A", order=1, logo=SimpleUploadedFile("l.png", b"i"))
        partners = list(ValuedPartner.objects.all())
        self.assertEqual(partners[0].name, "A")
        self.assertEqual(partners[1].name, "B")


class NewsCategoryModelTests(TestCase):
    def test_create_category(self):
        cat = NewsCategory.objects.create(name="Press Release")
        self.assertEqual(str(cat), "Press Release")

    def test_auto_order(self):
        cat1 = NewsCategory.objects.create(name="First")
        self.assertEqual(cat1.order, 1)
        cat2 = NewsCategory.objects.create(name="Second")
        self.assertEqual(cat2.order, 2)


class NewsModelTests(TestCase):
    def setUp(self):
        self.category = NewsCategory.objects.create(name="News")

    def test_create_news(self):
        news = News.objects.create(title="Test Article", news_category=self.category, news_date=date.today())
        self.assertEqual(str(news), "Test Article")

    def test_published_auto_sets_published_at(self):
        news = News.objects.create(title="Published", news_category=self.category, news_date=date.today(), is_published=True)
        self.assertIsNotNone(news.published_at)

    def test_unpublished_clears_published_at(self):
        news = News.objects.create(title="Unpub", news_category=self.category, news_date=date.today(), is_published=True)
        self.assertIsNotNone(news.published_at)
        news.is_published = False
        news.save()
        self.assertIsNone(news.published_at)

    def test_default_ordering(self):
        n1 = News.objects.create(title="Older", news_category=self.category, news_date=date(2024, 1, 1))
        n2 = News.objects.create(title="Newer", news_category=self.category, news_date=date(2025, 1, 1))
        self.assertEqual(list(News.objects.all()), [n2, n1])


class NewsAttachmentModelTests(TestCase):
    def setUp(self):
        self.category = NewsCategory.objects.create(name="News")
        self.news = News.objects.create(title="Article", news_category=self.category, news_date=date.today())

    def test_create_attachment(self):
        attachment = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("doc.pdf", b"content"), title="Report")
        self.assertEqual(str(attachment), "Report")

    def test_cascade_delete(self):
        NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("doc.pdf", b"content"), title="Doc")
        self.assertEqual(NewsAttachment.objects.count(), 1)
        self.news.delete()
        self.assertEqual(NewsAttachment.objects.count(), 0)


# ─── Serializer Tests ──────────────────────────────────────────────

class BannerSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"headline": "Hero", "subheadline": "Sub", "typewriter_words": ["fast"]}
        serializer = BannerCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_fields(self):
        banner = Banner.objects.create(headline="Test")
        serializer = BannerListSerializer(banner)
        self.assertIn("id", serializer.data)
        self.assertIn("headline", serializer.data)
        self.assertIn("background_image", serializer.data)

    def test_detail_serializer(self):
        banner = Banner.objects.create(headline="Test")
        serializer = BannerDetailSerializer(banner)
        self.assertIn("headline", serializer.data)


class NewsSerializerTests(TestCase):
    def setUp(self):
        self.category = NewsCategory.objects.create(name="News")

    def test_create_serializer_valid(self):
        data = {"title": "Test", "news_category_id": self.category.pk, "news_date": "2025-01-01", "is_published": False}
        serializer = NewsCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_invalid_category(self):
        data = {"title": "Test", "news_category_id": 9999, "news_date": "2025-01-01"}
        serializer = NewsCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("news_category_id", serializer.errors)

    def test_list_serializer_fields(self):
        news = News.objects.create(title="Article", news_category=self.category, news_date=date.today())
        serializer = NewsListSerializer(news)
        self.assertIn("id", serializer.data)
        self.assertIn("image", serializer.data)

    def test_retrieve_serializer_fields(self):
        news = News.objects.create(title="Article", news_category=self.category, news_date=date.today())
        serializer = NewsRetrieveSerializer(news)
        self.assertIn("content_html", serializer.data)
        self.assertIn("published_at", serializer.data)


class NewsCategorySerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"name": "Events", "order": 5}
        serializer = NewsCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer(self):
        cat = NewsCategory.objects.create(name="News")
        serializer = NewsCategoryListSerializer(cat)
        self.assertIn("id", serializer.data)
        self.assertIn("name", serializer.data)


class NewsAttachmentSerializerTests(TestCase):
    def setUp(self):
        self.category = NewsCategory.objects.create(name="News")
        self.news = News.objects.create(title="Article", news_category=self.category, news_date=date.today())

    def test_create_serializer_valid(self):
        data = {"news_id": self.news.pk, "file": SimpleUploadedFile("doc.pdf", b"content"), "title": "Doc"}
        serializer = NewsAttachmentCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_detail_serializer_fields(self):
        att = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("doc.pdf", b"c"), title="Doc")
        serializer = NewsAttachmentDetailSerializer(att)
        self.assertIn("file", serializer.data)
        self.assertIn("title", serializer.data)


class SiteSettingsSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"company_name": "TAC Hydro", "founded_year": 2000}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_phone_validation_valid(self):
        data = {"company_name": "TAC", "phone": "+977-1-4222832"}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_phone_validation_invalid(self):
        data = {"company_name": "TAC", "phone": "invalid!!!"}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_linkedin_url_validation(self):
        data = {"company_name": "TAC", "linkedin_url": "https://example.com"}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("linkedin_url", serializer.errors)

    def test_facebook_url_validation(self):
        data = {"company_name": "TAC", "facebook_url": "https://example.com"}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("facebook_url", serializer.errors)

    def test_founded_year_valid(self):
        data = {"company_name": "TAC", "founded_year": date.today().year}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_founded_year_too_old(self):
        data = {"company_name": "TAC", "founded_year": 1799}
        serializer = SiteSettingsCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("founded_year", serializer.errors)


class ValuedPartnerSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"name": "Partner A", "order": 1, "logo": SimpleUploadedFile("logo.png", b"img")}
        serializer = ValuedPartnerCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_logo_url(self):
        partner = ValuedPartner.objects.create(name="P", order=1, logo=SimpleUploadedFile("l.png", b"i"))
        serializer = ValuedPartnerListSerializer(partner)
        self.assertIn("logo", serializer.data)


# ─── View Tests ────────────────────────────────────────────────────

class BannerViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.b1 = Banner.objects.create(headline="B1")
        self.b2 = Banner.objects.create(headline="B2")

    def test_list_banners(self):
        response = self.client.get(reverse("banner-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_banner(self):
        data = {"headline": "New Banner", "subheadline": "Sub", "typewriter_words": ["a"]}
        response = self.client.post(reverse("banner-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Banner.objects.count(), 3)

    def test_retrieve_banner(self):
        response = self.client.get(reverse("banner-detail", args=[self.b1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["headline"], "B1")

    def test_update_banner(self):
        response = self.client.put(
            reverse("banner-detail", args=[self.b1.pk]),
            {"headline": "Updated", "subheadline": "", "typewriter_words": []},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_banner(self):
        response = self.client.delete(reverse("banner-detail", args=[self.b1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Banner.objects.count(), 1)

    def test_unauthenticated_read_allowed(self):
        client = APIClient()
        response = client.get(reverse("banner-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_write_denied(self):
        client = APIClient()
        response = client.post(reverse("banner-list"), {"headline": "Test"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_background_image_upload(self):
        img = SimpleUploadedFile("bg.jpg", b"image_content", content_type="image/jpeg")
        response = self.client.post(
            reverse("banner-background-image", args=[self.b1.pk]),
            {"file": img},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Banner.objects.get(pk=self.b1.pk).background_image)

    def test_background_image_no_file(self):
        response = self.client.post(
            reverse("banner-background-image", args=[self.b1.pk]),
            {},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NewsViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.category = NewsCategory.objects.create(name="News")
        self.n1 = News.objects.create(title="N1", news_category=self.category, news_date=date(2025, 1, 1), is_published=True)
        self.n2 = News.objects.create(title="N2", news_category=self.category, news_date=date(2025, 2, 1), is_published=False)

    def test_list_news(self):
        response = self.client.get(reverse("news-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_filter_by_published(self):
        response = self.client.get(reverse("news-list") + "?is_published=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_by_category(self):
        response = self.client.get(reverse("news-list") + f"?news_category_id={self.category.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_news(self):
        data = {"title": "New Article", "news_category_id": self.category.pk, "news_date": "2025-03-01", "is_published": True}
        response = self.client.post(reverse("news-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 3)

    def test_retrieve_news(self):
        response = self.client.get(reverse("news-detail", args=[self.n1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "N1")

    def test_update_news(self):
        data = {"title": "Updated", "news_category_id": self.category.pk, "news_date": "2025-03-01"}
        response = self.client.put(reverse("news-detail", args=[self.n1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_news(self):
        response = self.client.delete(reverse("news-detail", args=[self.n1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_counts_action(self):
        response = self.client.get(reverse("news-counts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("all", response.data)
        self.assertIn("published", response.data)
        self.assertIn("drafts", response.data)
        self.assertIn("by_category", response.data)

    def test_image_upload(self):
        img = SimpleUploadedFile("news.jpg", b"image_content", content_type="image/jpeg")
        response = self.client.post(
            reverse("news-upload-image", args=[self.n1.pk]),
            {"file": img},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(News.objects.get(pk=self.n1.pk).image)

    def test_image_upload_no_file(self):
        response = self.client.post(
            reverse("news-upload-image", args=[self.n1.pk]),
            {},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_includes_attachments(self):
        att = NewsAttachment.objects.create(
            news=self.n1, file=SimpleUploadedFile("doc.pdf", b"content"), title="Report"
        )
        response = self.client.get(reverse("news-detail", args=[self.n1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("attachments", response.data)
        self.assertEqual(len(response.data["attachments"]), 1)
        self.assertEqual(response.data["attachments"][0]["id"], att.pk)
        self.assertEqual(response.data["attachments"][0]["title"], "Report")
        self.assertIn("file", response.data["attachments"][0])


class NewsCategoryViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.c1 = NewsCategory.objects.create(name="Cat1")
        self.c2 = NewsCategory.objects.create(name="Cat2")

    def test_list(self):
        response = self.client.get(reverse("newscategory-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(reverse("newscategory-list"), {"name": "Cat3"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("newscategory-detail", args=[self.c1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put(reverse("newscategory-detail", args=[self.c1.pk]), {"name": "Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("newscategory-detail", args=[self.c1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NewsAttachmentViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.category = NewsCategory.objects.create(name="News")
        self.news = News.objects.create(title="Article", news_category=self.category, news_date=date.today())

    def test_list(self):
        att = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("d.pdf", b"c"), title="Doc")
        response = self.client.get(reverse("newsattachment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve(self):
        att = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("d.pdf", b"c"), title="Doc")
        response = self.client.get(reverse("newsattachment-detail", args=[att.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_with_file(self):
        response = self.client.post(
            reverse("newsattachment-list"),
            {
                "news_id": self.news.pk,
                "file": SimpleUploadedFile("report.pdf", b"pdf_content"),
                "title": "Annual Report",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsAttachment.objects.count(), 1)
        self.assertEqual(response.data["title"], "Annual Report")

    def test_create_without_file_returns_400(self):
        response = self.client.post(
            reverse("newsattachment-list"),
            {"news_id": self.news.pk, "file": "", "title": "No File"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_title_only(self):
        att = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("d.pdf", b"c"), title="Original")
        response = self.client.patch(
            reverse("newsattachment-detail", args=[att.pk]),
            {"title": "Updated Title"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        att.refresh_from_db()
        self.assertEqual(att.title, "Updated Title")

    def test_list_filter_by_news_id(self):
        other_news = News.objects.create(title="Other", news_category=self.category, news_date=date.today())
        a1 = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("a.pdf", b"a"), title="A")
        NewsAttachment.objects.create(news=other_news, file=SimpleUploadedFile("b.pdf", b"b"), title="B")
        response = self.client.get(reverse("newsattachment-list"), {"news_id": self.news.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], a1.pk)

    def test_delete(self):
        att = NewsAttachment.objects.create(news=self.news, file=SimpleUploadedFile("d.pdf", b"c"), title="Doc")
        response = self.client.delete(reverse("newsattachment-detail", args=[att.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SiteSettingsViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.s = SiteSettings.objects.create(company_name="TAC Hydro")

    def test_list(self):
        response = self.client.get(reverse("sitesettings-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create(self):
        data = {"company_name": "New Co", "founded_year": 2000}
        response = self.client.post(reverse("sitesettings-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SiteSettings.objects.count(), 2)

    def test_retrieve(self):
        response = self.client.get(reverse("sitesettings-detail", args=[self.s.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "TAC Hydro")

    def test_update(self):
        response = self.client.put(
            reverse("sitesettings-detail", args=[self.s.pk]),
            {"company_name": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("sitesettings-detail", args=[self.s.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_organization_chart_image_upload(self):
        img = SimpleUploadedFile("chart.png", b"image_content", content_type="image/png")
        response = self.client.post(
            reverse("sitesettings-organization-chart-image", args=[self.s.pk]),
            {"organization_chart_image": img},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(SiteSettings.objects.get(pk=self.s.pk).organization_chart_image)

    def test_organization_chart_image_no_file(self):
        response = self.client.post(
            reverse("sitesettings-organization-chart-image", args=[self.s.pk]),
            {},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ValuedPartnerViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.p1 = ValuedPartner.objects.create(name="P1", order=1, logo=SimpleUploadedFile("l.png", b"i"))
        self.p2 = ValuedPartner.objects.create(name="P2", order=2, logo=SimpleUploadedFile("l.png", b"i"))

    def test_list(self):
        response = self.client.get(reverse("valuedpartner-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(
            reverse("valuedpartner-list"),
            {"name": "P3", "logo": SimpleUploadedFile("l.png", b"i")},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("valuedpartner-detail", args=[self.p1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put(
            reverse("valuedpartner-detail", args=[self.p1.pk]),
            {"name": "Updated", "logo": SimpleUploadedFile("l.png", b"i")},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("valuedpartner-detail", args=[self.p1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class StatsViewTests(TestCase):
    def test_stats_returns_expected_keys(self):
        client = APIClient()
        response = client.get("/api/home/stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("mw_capacity", response.data)
        self.assertIn("projects_count", response.data)
        self.assertIn("clients_count", response.data)
        self.assertIn("team_members_count", response.data)
        self.assertIn("years", response.data)


class TokenViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="admin@example.com", username="admin", password="secret123")

    def test_login_success(self):
        client = APIClient()
        response = client.post("/api/auth/token/", {"email": "admin@example.com", "password": "secret123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_missing_fields(self):
        client = APIClient()
        response = client.post("/api/auth/token/", {"email": "test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_credentials(self):
        client = APIClient()
        response = client.post(
            "/api/auth/token/",
            {"email": "admin@example.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenValidateViewTests(TestCase):
    def test_valid_token(self):
        user = User.objects.create_user(email="admin@example.com", username="admin", password="secret")
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = client.post("/api/auth/validate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_valid"])

    def test_no_token(self):
        client = APIClient()
        response = client.post("/api/auth/validate/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── Admin Dashboard Stats View Tests ─────────────────────────────

class AdminDashboardStatsViewTests(TestCase):
    def test_authenticated_returns_correct_counts(self):
        client, _ = create_authenticated_client()
        TeamMember.objects.create(name="Alice", is_active=True)
        TeamMember.objects.create(name="Bob", is_active=True)
        scope = ProjectScope.objects.create(name="Feasibility")
        project = Project.objects.create(
            title="Test Project", installed_capacity=1.0, latitude=0, longitude=0,
        )
        ProjectScopeMembership.objects.create(project=project, project_scope=scope)
        ServiceSector.objects.create(title="Energy")
        ExpertiseCategory.objects.create(title="Hydropower", icon_key="dam")
        News.objects.create(
            title="News Item",
            news_category=NewsCategory.objects.create(name="Updates"),
            news_date=date.today(),
        )
        ValuedPartner.objects.create(name="Partner A", order=1)

        response = client.get("/api/home/admin-stats/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["team_members_count"], 2)
        self.assertEqual(response.data["projects_count"], 1)
        self.assertEqual(response.data["projects_by_scope"], {"Feasibility": 1})
        self.assertEqual(response.data["service_sectors_count"], 1)
        self.assertEqual(response.data["expertise_categories_count"], 1)
        self.assertEqual(response.data["news_count"], 1)
        self.assertEqual(response.data["partners_count"], 1)

    def test_projects_by_scope_breakdown(self):
        client, _ = create_authenticated_client()
        scope_a = ProjectScope.objects.create(name="Feasibility")
        scope_b = ProjectScope.objects.create(name="Construction")
        p1 = Project.objects.create(title="P1", installed_capacity=1, latitude=0, longitude=0)
        p2 = Project.objects.create(title="P2", installed_capacity=1, latitude=0, longitude=0)
        p3 = Project.objects.create(title="P3", installed_capacity=1, latitude=0, longitude=0)
        ProjectScopeMembership.objects.create(project=p1, project_scope=scope_a)
        ProjectScopeMembership.objects.create(project=p2, project_scope=scope_a)
        ProjectScopeMembership.objects.create(project=p3, project_scope=scope_b)

        response = client.get("/api/home/admin-stats/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data["projects_by_scope"],
            {"Feasibility": 2, "Construction": 1},
        )

    def test_only_active_team_members_counted(self):
        client, _ = create_authenticated_client()
        TeamMember.objects.create(name="Active One", is_active=True)
        TeamMember.objects.create(name="Inactive One", is_active=False)

        response = client.get("/api/home/admin-stats/")

        self.assertEqual(response.data["team_members_count"], 1)

    def test_unauthenticated_returns_401(self):
        client = APIClient()
        response = client.get("/api/home/admin-stats/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── Change Password View Tests ───────────────────────────────────

class ChangePasswordViewTests(TestCase):
    def test_successful_change(self):
        client, user = create_authenticated_client()
        old_password = "testpass123"
        new_password = "NewStr0ng!Pass"

        response = client.post("/api/auth/change-password/", {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_password": new_password,
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"success": True})

        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))
        self.assertFalse(user.check_password(old_password))

    def test_missing_old_password(self):
        client, _ = create_authenticated_client()
        response = client.post("/api/auth/change-password/", {
            "new_password": "NewStr0ng!Pass",
            "confirm_password": "NewStr0ng!Pass",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data)

    def test_missing_new_password(self):
        client, _ = create_authenticated_client()
        response = client.post("/api/auth/change-password/", {
            "old_password": "testpass123",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)

    def test_wrong_old_password(self):
        client, _ = create_authenticated_client()
        response = client.post("/api/auth/change-password/", {
            "old_password": "wrongpassword",
            "new_password": "NewStr0ng!Pass",
            "confirm_password": "NewStr0ng!Pass",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data)

    def test_passwords_do_not_match(self):
        client, _ = create_authenticated_client()
        response = client.post("/api/auth/change-password/", {
            "old_password": "testpass123",
            "new_password": "NewStr0ng!Pass",
            "confirm_password": "Mismatch123!",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)

    def test_weak_new_password(self):
        client, _ = create_authenticated_client()
        response = client.post("/api/auth/change-password/", {
            "old_password": "testpass123",
            "new_password": "12345678",
            "confirm_password": "12345678",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)

    def test_unauthenticated_returns_401(self):
        client = APIClient()
        response = client.post("/api/auth/change-password/", {
            "old_password": "testpass123",
            "new_password": "NewStr0ng!Pass",
            "confirm_password": "NewStr0ng!Pass",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
