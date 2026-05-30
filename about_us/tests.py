from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from about_us.models import (
    AboutPageSection,
    CorePrinciple,
    CorePrinciplesIntro,
    TeamCategory,
    TeamMember,
    TeamMemberCategory,
)
from about_us.serializers.about_page_section import (
    AboutPageSectionCreateSerializer,
    AboutPageSectionDetailSerializer,
    AboutPageSectionListSerializer,
    AboutPageSectionUpdateSerializer,
)
from about_us.serializers.core_principle import (
    CorePrincipleCreateSerializer,
    CorePrincipleDetailSerializer,
    CorePrincipleListSerializer,
    CorePrincipleUpdateSerializer,
)
from about_us.serializers.core_principles_intro import (
    CorePrinciplesIntroCreateSerializer,
    CorePrinciplesIntroDetailSerializer,
    CorePrinciplesIntroListSerializer,
    CorePrinciplesIntroUpdateSerializer,
)
from about_us.serializers.team_category import (
    TeamCategoryCreateSerializer,
    TeamCategoryDetailSerializer,
    TeamCategoryListSerializer,
    TeamCategoryUpdateSerializer,
)
from about_us.serializers.team_member import (
    TeamMemberCreateSerializer,
    TeamMemberDetailSerializer,
    TeamMemberListSerializer,
    TeamMemberUpdateSerializer,
)
from about_us.serializers.team_member_category import (
    TeamMemberCategoryCreateSerializer,
    TeamMemberCategoryDetailSerializer,
    TeamMemberCategoryListSerializer,
    TeamMemberCategoryUpdateSerializer,
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


# ─── Model Tests ───────────────────────────────────────────────────

class AboutPageSectionModelTests(TestCase):
    def test_create(self):
        section = AboutPageSection.objects.create(section_key="mission", title="Our Mission", content_html="<p>Mission</p>")
        self.assertEqual(str(section), "Our Mission")

    def test_section_key_unique(self):
        AboutPageSection.objects.create(section_key="vision", title="Vision")
        with self.assertRaises(Exception):
            AboutPageSection.objects.create(section_key="vision", title="Duplicate")


class CorePrinciplesIntroModelTests(TestCase):
    def test_create(self):
        intro = CorePrinciplesIntro.objects.create(title="Our Principles")
        self.assertEqual(str(intro), "Our Principles")


class CorePrincipleModelTests(TestCase):
    def test_create(self):
        cp = CorePrinciple.objects.create(title="Integrity", description="We act with integrity", icon_key="handshake", color_class="blue")
        self.assertEqual(str(cp), "Integrity")

    def test_default_ordering(self):
        CorePrinciple.objects.create(title="B", icon_key="b", color_class="red", order=2)
        CorePrinciple.objects.create(title="A", icon_key="a", color_class="red", order=1)
        self.assertEqual(
            list(CorePrinciple.objects.all()),
            [
                CorePrinciple.objects.get(title="A"),
                CorePrinciple.objects.get(title="B"),
            ],
        )


class TeamCategoryModelTests(TestCase):
    def test_create(self):
        cat = TeamCategory.objects.create(name="Engineering")
        self.assertEqual(str(cat), "Engineering")


class TeamMemberModelTests(TestCase):
    def test_create(self):
        member = TeamMember.objects.create(name="John Doe", education="MIT", is_active=True)
        self.assertEqual(str(member), "John Doe")

    def test_inactive_member(self):
        TeamMember.objects.create(name="Inactive", is_active=False)
        active = TeamMember.objects.filter(is_active=True).count()
        self.assertEqual(active, 0)


class TeamMemberCategoryModelTests(TestCase):
    def setUp(self):
        self.member = TeamMember.objects.create(name="John")
        self.category = TeamCategory.objects.create(name="Engineers")

    def test_create(self):
        tmc = TeamMemberCategory.objects.create(team_member=self.member, category=self.category, technical_expertise="Hydropower", role="Lead")
        self.assertIn("John", str(tmc))
        self.assertIn("Engineers", str(tmc))

    def test_cascade_delete_member(self):
        TeamMemberCategory.objects.create(team_member=self.member, category=self.category, technical_expertise="Hydro")
        self.assertEqual(TeamMemberCategory.objects.count(), 1)
        self.member.delete()
        self.assertEqual(TeamMemberCategory.objects.count(), 0)

    def test_cascade_delete_category(self):
        TeamMemberCategory.objects.create(team_member=self.member, category=self.category, technical_expertise="Hydro")
        self.assertEqual(TeamMemberCategory.objects.count(), 1)
        self.category.delete()
        self.assertEqual(TeamMemberCategory.objects.count(), 0)


# ─── Serializer Tests ──────────────────────────────────────────────

class AboutPageSectionSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"section_key": "story", "title": "Our Story"}
        serializer = AboutPageSectionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer(self):
        section = AboutPageSection.objects.create(section_key="test", title="Test")
        serializer = AboutPageSectionListSerializer(section)
        self.assertIn("id", serializer.data)
        self.assertIn("section_key", serializer.data)
        self.assertIn("image", serializer.data)


class CorePrinciplesIntroSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"title": "Intro"}
        serializer = CorePrinciplesIntroCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_image(self):
        intro = CorePrinciplesIntro.objects.create(title="Intro")
        serializer = CorePrinciplesIntroListSerializer(intro)
        self.assertIn("image", serializer.data)
        self.assertIsNone(serializer.data["image"])


class CorePrincipleSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"title": "Excellence", "icon_key": "star", "color_class": "gold", "order": 1}
        serializer = CorePrincipleCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_fields(self):
        cp = CorePrinciple.objects.create(title="T", icon_key="i", color_class="c")
        serializer = CorePrincipleListSerializer(cp)
        self.assertIn("id", serializer.data)
        self.assertIn("title", serializer.data)
        self.assertIn("description", serializer.data)
        self.assertIn("icon_key", serializer.data)
        self.assertIn("color_class", serializer.data)
        self.assertIn("order", serializer.data)


class TeamCategorySerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"name": "Management", "order": 1}
        serializer = TeamCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class TeamMemberSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"name": "Jane", "education": "Harvard", "is_active": True}
        serializer = TeamMemberCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_photos(self):
        member = TeamMember.objects.create(name="Jane")
        serializer = TeamMemberListSerializer(member)
        self.assertIn("photo", serializer.data)
        self.assertIn("profile_photo", serializer.data)
        self.assertIsNone(serializer.data["photo"])
        self.assertIsNone(serializer.data["profile_photo"])


class TeamMemberCategorySerializerTests(TestCase):
    def setUp(self):
        self.member = TeamMember.objects.create(name="John")
        self.category = TeamCategory.objects.create(name="Engineers")

    def test_create_serializer_valid(self):
        data = {"team_member_id": self.member.pk, "category_id": self.category.pk, "technical_expertise": "Hydro", "role": "Lead"}
        serializer = TeamMemberCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_invalid_member(self):
        data = {"team_member_id": 9999, "category_id": self.category.pk, "technical_expertise": "Hydro"}
        serializer = TeamMemberCategoryCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("team_member_id", serializer.errors)

    def test_list_serializer_fields(self):
        tmc = TeamMemberCategory.objects.create(team_member=self.member, category=self.category, technical_expertise="Hydro")
        serializer = TeamMemberCategoryListSerializer(tmc)
        self.assertIn("team_member_id", serializer.data)
        self.assertIn("category_id", serializer.data)
        self.assertIn("technical_expertise", serializer.data)


# ─── View Tests ────────────────────────────────────────────────────

class AboutPageSectionViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.s1 = AboutPageSection.objects.create(section_key="mission", title="Mission")
        self.s2 = AboutPageSection.objects.create(section_key="vision", title="Vision")

    def test_list(self):
        response = self.client.get(reverse("aboutpagesection-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        data = {"section_key": "story", "title": "Story"}
        response = self.client.post(reverse("aboutpagesection-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("aboutpagesection-detail", args=[self.s1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["section_key"], "mission")

    def test_update(self):
        response = self.client.put(
            reverse("aboutpagesection-detail", args=[self.s1.pk]),
            {"section_key": "mission", "title": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AboutPageSection.objects.get(pk=self.s1.pk).title, "Updated")

    def test_delete(self):
        response = self.client.delete(reverse("aboutpagesection-detail", args=[self.s1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_read_allowed(self):
        client = APIClient()
        response = client.get(reverse("aboutpagesection-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_write_denied(self):
        client = APIClient()
        response = client.post(reverse("aboutpagesection-list"), {"section_key": "t", "title": "T"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_image_upload(self):
        img = SimpleUploadedFile("section.png", b"content", content_type="image/png")
        response = self.client.post(
            reverse("aboutpagesection-upload-image", args=[self.s1.pk]),
            {"file": img},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(AboutPageSection.objects.get(pk=self.s1.pk).image)

    def test_image_upload_no_file(self):
        response = self.client.post(
            reverse("aboutpagesection-upload-image", args=[self.s1.pk]),
            {},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CorePrinciplesIntroViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.i1 = CorePrinciplesIntro.objects.create(title="Intro")

    def test_list(self):
        response = self.client.get(reverse("coreprinciplesintro-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create(self):
        data = {"title": "New Intro"}
        response = self.client.post(reverse("coreprinciplesintro-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("coreprinciplesintro-detail", args=[self.i1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put(reverse("coreprinciplesintro-detail", args=[self.i1.pk]), {"title": "U"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("coreprinciplesintro-detail", args=[self.i1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_image_upload(self):
        img = SimpleUploadedFile("intro.png", b"c", content_type="image/png")
        response = self.client.post(
            reverse("coreprinciplesintro-upload-image", args=[self.i1.pk]),
            {"file": img},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(CorePrinciplesIntro.objects.get(pk=self.i1.pk).image)


class CorePrincipleViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.c1 = CorePrinciple.objects.create(title="Integrity", icon_key="handshake", color_class="blue", order=1)
        self.c2 = CorePrinciple.objects.create(title="Excellence", icon_key="star", color_class="gold", order=2)

    def test_list(self):
        response = self.client.get(reverse("coreprinciple-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        data = {"title": "New", "icon_key": "key", "color_class": "red", "order": 3}
        response = self.client.post(reverse("coreprinciple-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("coreprinciple-detail", args=[self.c1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {"title": "Updated", "icon_key": "key", "color_class": "blue", "order": 1}
        response = self.client.put(reverse("coreprinciple-detail", args=[self.c1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("coreprinciple-detail", args=[self.c1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TeamCategoryViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.t1 = TeamCategory.objects.create(name="Engineers", order=1)
        self.t2 = TeamCategory.objects.create(name="Managers", order=2)

    def test_list(self):
        response = self.client.get(reverse("teamcategory-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(reverse("teamcategory-list"), {"name": "New"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("teamcategory-detail", args=[self.t1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put(reverse("teamcategory-detail", args=[self.t1.pk]), {"name": "U"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("teamcategory-detail", args=[self.t1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TeamMemberViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.m1 = TeamMember.objects.create(name="John", is_active=True)
        self.m2 = TeamMember.objects.create(name="Jane", is_active=False)

    def test_list(self):
        response = self.client.get(reverse("teammember-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        data = {"name": "New Member", "is_active": True}
        response = self.client.post(reverse("teammember-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("teammember-detail", args=[self.m1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {"name": "Updated", "is_active": True}
        response = self.client.put(reverse("teammember-detail", args=[self.m1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("teammember-detail", args=[self.m1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TeamMemberCategoryViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.member = TeamMember.objects.create(name="John")
        self.category = TeamCategory.objects.create(name="Engineers")
        self.tmc = TeamMemberCategory.objects.create(team_member=self.member, category=self.category, technical_expertise="Hydro")

    def test_list(self):
        response = self.client.get(reverse("teammembercategory-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create(self):
        data = {"team_member_id": self.member.pk, "category_id": self.category.pk, "technical_expertise": "Solar", "role": "Lead"}
        response = self.client.post(reverse("teammembercategory-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(reverse("teammembercategory-detail", args=[self.tmc.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["technical_expertise"], "Hydro")

    def test_update(self):
        data = {"team_member_id": self.member.pk, "category_id": self.category.pk, "technical_expertise": "Updated"}
        response = self.client.put(reverse("teammembercategory-detail", args=[self.tmc.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("teammembercategory-detail", args=[self.tmc.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_member_returns_400(self):
        data = {"team_member_id": 9999, "category_id": self.category.pk, "technical_expertise": "Hydro"}
        response = self.client.post(reverse("teammembercategory-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
