from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from projects.models import Project, ProjectScope, ProjectScopeImage, ProjectScopeMembership
from projects.serializers.project import (
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectUpdateSerializer,
)
from projects.serializers.project_scope import (
    ProjectScopeCreateSerializer,
    ProjectScopeDetailSerializer,
    ProjectScopeListSerializer,
    ProjectScopeUpdateSerializer,
)
from projects.serializers.project_scope_image import (
    ProjectScopeImageCreateSerializer,
    ProjectScopeImageDetailSerializer,
    ProjectScopeImageListSerializer,
    ProjectScopeImageUpdateSerializer,
)
from projects.serializers.project_scope_membership import (
    ProjectScopeMembershipCreateSerializer,
    ProjectScopeMembershipDetailSerializer,
    ProjectScopeMembershipListSerializer,
    ProjectScopeMembershipUpdateSerializer,
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


SCOPE_LIST = "/api/projects/scopes/"
SCOPE_DETAIL = lambda pk: f"/api/projects/scopes/{pk}/"
MEMBERSHIP_LIST = "/api/projects/scope-memberships/"
MEMBERSHIP_DETAIL = lambda pk: f"/api/projects/scope-memberships/{pk}/"
IMAGE_LIST = "/api/projects/scope-images/"
IMAGE_DETAIL = lambda pk: f"/api/projects/scope-images/{pk}/"


# ─── Model Tests ───────────────────────────────────────────────────

class ProjectModelTests(TestCase):
    def test_create(self):
        p = Project.objects.create(
            title="Dam Project",
            status="Completed",
            installed_capacity=150.0,
            latitude=27.5,
            longitude=85.3,
        )
        self.assertEqual(str(p), "Dam Project")

    def test_all_fields(self):
        p = Project.objects.create(
            title="Hydro",
            status="Ongoing",
            installed_capacity=75.5,
            installed_capacity_unit="MW",
            latitude=28.0,
            longitude=84.0,
            description="A hydro project",
            technical_highlights={"turbine": "Kaplan"},
        )
        self.assertEqual(p.installed_capacity_unit, "MW")
        self.assertEqual(p.technical_highlights, {"turbine": "Kaplan"})

    def test_status_choices(self):
        Project.objects.create(title="C", status="Completed", installed_capacity=1, latitude=0, longitude=0)
        Project.objects.create(title="O", status="Ongoing", installed_capacity=1, latitude=0, longitude=0)
        self.assertEqual(Project.objects.count(), 2)


class ProjectScopeModelTests(TestCase):
    def test_create(self):
        scope = ProjectScope.objects.create(name="Feasibility", order=1)
        self.assertEqual(str(scope), "Feasibility")

    def test_default_ordering(self):
        ProjectScope.objects.create(name="B", order=2)
        ProjectScope.objects.create(name="A", order=1)
        scopes = list(ProjectScope.objects.all())
        self.assertEqual(scopes[0].name, "A")


class ProjectScopeMembershipModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title="P", installed_capacity=1, latitude=0, longitude=0)
        self.scope = ProjectScope.objects.create(name="Feasibility")

    def test_create(self):
        m = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)
        self.assertIn("P", str(m))

    def test_unique_together(self):
        ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)
        with self.assertRaises(Exception):
            ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)

    def test_role(self):
        m = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope, role="Lead")
        self.assertEqual(m.role, "Lead")


class ProjectScopeImageModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title="P", installed_capacity=1, latitude=0, longitude=0)
        self.scope = ProjectScope.objects.create(name="Feasibility")
        self.membership = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)

    def test_create(self):
        img = ProjectScopeImage.objects.create(
            project_scope_membership=self.membership,
            image=SimpleUploadedFile("img.jpg", b"data"),
            alt_text="Photo",
            order=1,
        )
        self.assertIn("image 1", str(img))

    def test_max_four_images(self):
        for i in range(4):
            ProjectScopeImage.objects.create(
                project_scope_membership=self.membership,
                image=SimpleUploadedFile(f"img{i}.jpg", b"data"),
                order=i,
            )
        img5 = ProjectScopeImage(
            project_scope_membership=self.membership,
            image=SimpleUploadedFile("img5.jpg", b"data"),
            order=5,
        )
        with self.assertRaises(ValidationError):
            img5.full_clean()

    def test_cascade_on_membership_delete(self):
        ProjectScopeImage.objects.create(
            project_scope_membership=self.membership,
            image=SimpleUploadedFile("img.jpg", b"data"),
        )
        self.assertEqual(ProjectScopeImage.objects.count(), 1)
        self.membership.delete()
        self.assertEqual(ProjectScopeImage.objects.count(), 0)


# ─── Serializer Tests ──────────────────────────────────────────────

class ProjectSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"title": "New", "installed_capacity": 50, "latitude": 27.0, "longitude": 85.0}
        serializer = ProjectCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_fields(self):
        p = Project.objects.create(title="Test", installed_capacity=1, latitude=0, longitude=0)
        serializer = ProjectListSerializer(p)
        self.assertIn("id", serializer.data)
        self.assertIn("title", serializer.data)
        self.assertNotIn("description", serializer.data)

    def test_detail_serializer_fields(self):
        p = Project.objects.create(title="Test", installed_capacity=1, latitude=0, longitude=0, description="Desc")
        serializer = ProjectDetailSerializer(p)
        self.assertIn("description", serializer.data)
        self.assertIn("technical_highlights", serializer.data)


class ProjectScopeSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"name": "Design", "order": 2}
        serializer = ProjectScopeCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer(self):
        s = ProjectScope.objects.create(name="Test")
        serializer = ProjectScopeListSerializer(s)
        self.assertIn("id", serializer.data)
        self.assertIn("name", serializer.data)


class ProjectScopeMembershipSerializerTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title="P", installed_capacity=1, latitude=0, longitude=0)
        self.scope = ProjectScope.objects.create(name="Feasibility")

    def test_create_serializer_valid(self):
        data = {"project_id": self.project.pk, "project_scope_id": self.scope.pk, "role": "Lead"}
        serializer = ProjectScopeMembershipCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_invalid_project(self):
        data = {"project_id": 9999, "project_scope_id": self.scope.pk}
        serializer = ProjectScopeMembershipCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("project_id", serializer.errors)

    def test_list_serializer_image_urls(self):
        m = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)
        serializer = ProjectScopeMembershipListSerializer(m)
        self.assertIn("image_urls", serializer.data)
        self.assertEqual(serializer.data["image_urls"], [])


class ProjectScopeImageSerializerTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title="P", installed_capacity=1, latitude=0, longitude=0)
        self.scope = ProjectScope.objects.create(name="Feasibility")
        self.membership = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)

    def test_create_serializer_valid(self):
        data = {
            "project_scope_membership_id": self.membership.pk,
            "alt_text": "Photo",
            "order": 1,
            "image": SimpleUploadedFile("img.jpg", b"data"),
        }
        serializer = ProjectScopeImageCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_invalid_membership(self):
        data = {
            "project_scope_membership_id": 9999,
            "image": SimpleUploadedFile("img.jpg", b"data"),
        }
        serializer = ProjectScopeImageCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("project_scope_membership_id", serializer.errors)

    def test_list_serializer_image_url(self):
        img = ProjectScopeImage.objects.create(
            project_scope_membership=self.membership,
            image=SimpleUploadedFile("img.jpg", b"data"),
        )
        serializer = ProjectScopeImageListSerializer(img)
        self.assertIn("image", serializer.data)


# ─── View Tests ────────────────────────────────────────────────────

class ProjectViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.p1 = Project.objects.create(title="P1", installed_capacity=50, latitude=27.0, longitude=85.0)
        self.p2 = Project.objects.create(title="P2", installed_capacity=100, latitude=28.0, longitude=86.0)

    def test_list(self):
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        data = {"title": "New", "installed_capacity": 75, "latitude": 27.5, "longitude": 85.5}
        response = self.client.post(reverse("project-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 3)

    def test_retrieve(self):
        response = self.client.get(reverse("project-detail", args=[self.p1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "P1")

    def test_update(self):
        data = {"title": "Updated", "installed_capacity": 50, "latitude": 27.0, "longitude": 85.0}
        response = self.client.put(reverse("project-detail", args=[self.p1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("project-detail", args=[self.p1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_read_allowed(self):
        client = APIClient()
        response = client.get(reverse("project-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_write_denied(self):
        client = APIClient()
        response = client.post(reverse("project-list"), {"title": "T", "installed_capacity": 1, "latitude": 0, "longitude": 0})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProjectScopeViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.s1 = ProjectScope.objects.create(name="Feasibility", order=1)
        ProjectScope.objects.create(name="Design", order=2)

    def test_list(self):
        response = self.client.get(SCOPE_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(SCOPE_LIST, {"name": "Construction", "order": 3}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(SCOPE_DETAIL(self.s1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Feasibility")

    def test_update(self):
        response = self.client.put(SCOPE_DETAIL(self.s1.pk), {"name": "Updated", "order": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(SCOPE_DETAIL(self.s1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProjectScopeMembershipViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.project = Project.objects.create(title="P", installed_capacity=1, latitude=0, longitude=0)
        self.scope = ProjectScope.objects.create(name="Feasibility")
        self.m1 = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)

    def test_list(self):
        response = self.client.get(MEMBERSHIP_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create(self):
        scope2 = ProjectScope.objects.create(name="Design")
        data = {"project_id": self.project.pk, "project_scope_id": scope2.pk}
        response = self.client.post(MEMBERSHIP_LIST, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(MEMBERSHIP_DETAIL(self.m1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {"project_id": self.project.pk, "project_scope_id": self.scope.pk, "role": "Updated"}
        response = self.client.put(MEMBERSHIP_DETAIL(self.m1.pk), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(MEMBERSHIP_DETAIL(self.m1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_duplicate_returns_400(self):
        data = {"project_id": self.project.pk, "project_scope_id": self.scope.pk}
        response = self.client.post(MEMBERSHIP_LIST, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_project_returns_400(self):
        data = {"project_id": 9999, "project_scope_id": self.scope.pk}
        response = self.client.post(MEMBERSHIP_LIST, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProjectScopeImageViewTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.project = Project.objects.create(title="P", installed_capacity=1, latitude=0, longitude=0)
        self.scope = ProjectScope.objects.create(name="Feasibility")
        self.membership = ProjectScopeMembership.objects.create(project=self.project, project_scope=self.scope)
        self.img1 = ProjectScopeImage.objects.create(
            project_scope_membership=self.membership,
            image=SimpleUploadedFile("img.jpg", b"data"),
            order=1,
        )

    def test_list(self):
        response = self.client.get(IMAGE_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create(self):
        data = {
            "project_scope_membership_id": self.membership.pk,
            "order": 2,
            "image": SimpleUploadedFile("img2.jpg", b"data2"),
        }
        response = self.client.post(IMAGE_LIST, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectScopeImage.objects.count(), 2)

    def test_retrieve(self):
        response = self.client.get(IMAGE_DETAIL(self.img1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            "project_scope_membership_id": self.membership.pk,
            "order": 3,
            "image": SimpleUploadedFile("img3.jpg", b"data3"),
        }
        response = self.client.put(IMAGE_DETAIL(self.img1.pk), data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(IMAGE_DETAIL(self.img1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProjectScopeImage.objects.count(), 0)

    def test_invalid_membership_returns_400(self):
        data = {
            "project_scope_membership_id": 9999,
            "image": SimpleUploadedFile("img.jpg", b"d"),
        }
        response = self.client.post(IMAGE_LIST, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
