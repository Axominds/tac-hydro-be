from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from services.models import ExpertiseCategory, ExpertiseItem, ServiceSector
from projects.models import ProjectScope
from services.serializers.expertise_category import (
    ExpertiseCategoryCreateSerializer,
    ExpertiseCategoryDetailSerializer,
    ExpertiseCategoryListSerializer,
    ExpertiseCategoryUpdateSerializer,
)
from services.serializers.expertise_item import (
    ExpertiseItemCreateSerializer,
    ExpertiseItemDetailSerializer,
    ExpertiseItemListSerializer,
    ExpertiseItemUpdateSerializer,
)
from services.serializers.service_sector import (
    ServiceSectorCreateSerializer,
    ServiceSectorDetailSerializer,
    ServiceSectorListSerializer,
    ServiceSectorUpdateSerializer,
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

class ExpertiseCategoryModelTests(TestCase):
    def test_create(self):
        cat = ExpertiseCategory.objects.create(title="Civil Engineering", icon_key="bridge", order=1, theme_color="blue")
        self.assertEqual(str(cat), "Civil Engineering")

    def test_default_ordering(self):
        ExpertiseCategory.objects.create(title="B", icon_key="b", order=2)
        ExpertiseCategory.objects.create(title="A", icon_key="a", order=1)
        cats = list(ExpertiseCategory.objects.all())
        self.assertEqual(cats[0].title, "A")
        self.assertEqual(cats[1].title, "B")


class ExpertiseItemModelTests(TestCase):
    def setUp(self):
        self.category = ExpertiseCategory.objects.create(title="Civil", icon_key="c")
        self.scope = ProjectScope.objects.create(name="Feasibility")

    def test_create(self):
        item = ExpertiseItem.objects.create(category=self.category, title="Dam Design", project_scope=self.scope, order=1)
        self.assertEqual(str(item), "Dam Design")

    def test_optional_project_scope(self):
        item = ExpertiseItem.objects.create(category=self.category, title="General")
        self.assertIsNone(item.project_scope)


class ServiceSectorModelTests(TestCase):
    def test_create(self):
        sector = ServiceSector.objects.create(title="Hydropower", description="Hydro description", order=1)
        self.assertEqual(str(sector), "Hydropower")

    def test_default_ordering(self):
        ServiceSector.objects.create(title="B", order=2)
        ServiceSector.objects.create(title="A", order=1)
        sectors = list(ServiceSector.objects.all())
        self.assertEqual(sectors[0].title, "A")
        self.assertEqual(sectors[1].title, "B")


# ─── Serializer Tests ──────────────────────────────────────────────

class ExpertiseCategorySerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"title": "Mechanical", "icon_key": "gear", "order": 1}
        serializer = ExpertiseCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_fields(self):
        cat = ExpertiseCategory.objects.create(title="T", icon_key="i")
        serializer = ExpertiseCategoryListSerializer(cat)
        self.assertIn("id", serializer.data)
        self.assertIn("title", serializer.data)
        self.assertIn("icon_key", serializer.data)
        self.assertIn("order", serializer.data)
        self.assertIn("theme_color", serializer.data)


class ExpertiseItemSerializerTests(TestCase):
    def setUp(self):
        self.category = ExpertiseCategory.objects.create(title="Civil", icon_key="c")
        self.scope = ProjectScope.objects.create(name="Feasibility")

    def test_create_serializer_valid(self):
        data = {"category_id": self.category.pk, "title": "Dam Design", "project_scope_id": self.scope.pk, "order": 1}
        serializer = ExpertiseItemCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_without_project_scope(self):
        data = {"category_id": self.category.pk, "title": "General Item"}
        serializer = ExpertiseItemCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_invalid_scope(self):
        data = {"category_id": self.category.pk, "title": "Item", "project_scope_id": 9999}
        serializer = ExpertiseItemCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("project_scope_id", serializer.errors)

    def test_list_serializer_fields(self):
        item = ExpertiseItem.objects.create(category=self.category, title="Item")
        serializer = ExpertiseItemListSerializer(item)
        self.assertIn("id", serializer.data)
        self.assertIn("category_id", serializer.data)
        self.assertIn("title", serializer.data)
        self.assertIn("project_scope_id", serializer.data)


class ServiceSectorSerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"title": "Solar", "description": "Solar sector", "order": 1}
        serializer = ServiceSectorCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_image(self):
        sector = ServiceSector.objects.create(title="Wind")
        serializer = ServiceSectorListSerializer(sector)
        self.assertIn("image", serializer.data)
        self.assertIsNone(serializer.data["image"])


# ─── View Tests ────────────────────────────────────────────────────

class ServicesViewSetTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.cat1 = ExpertiseCategory.objects.create(title="Civil", icon_key="bridge", order=1)
        ExpertiseCategory.objects.create(title="Mechanical", icon_key="gear", order=2)
        self.scope = ProjectScope.objects.create(name="Feasibility")

    def test_list_categories(self):
        response = self.client.get(reverse("expertisecategory-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_category(self):
        data = {"title": "Electrical", "icon_key": "bolt", "order": 3}
        response = self.client.post(reverse("expertisecategory-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpertiseCategory.objects.count(), 3)

    def test_retrieve_category(self):
        response = self.client.get(reverse("expertisecategory-detail", args=[self.cat1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Civil")

    def test_update_category(self):
        data = {"title": "Updated", "icon_key": "bridge", "order": 1}
        response = self.client.put(reverse("expertisecategory-detail", args=[self.cat1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        response = self.client.delete(reverse("expertisecategory-detail", args=[self.cat1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExpertiseCategory.objects.count(), 1)

    def test_unauthenticated_read_allowed(self):
        client = APIClient()
        response = client.get(reverse("expertisecategory-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_write_denied(self):
        client = APIClient()
        response = client.post(reverse("expertisecategory-list"), {"title": "T", "icon_key": "k"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Nested Items

    def test_list_items(self):
        ExpertiseItem.objects.create(category=self.cat1, title="Item1")
        ExpertiseItem.objects.create(category=self.cat1, title="Item2")
        response = self.client.get(reverse("expertisecategory-items", args=[self.cat1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_item(self):
        data = {"category_id": self.cat1.pk, "title": "New Item", "order": 1}
        response = self.client.post(reverse("expertisecategory-items", args=[self.cat1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpertiseItem.objects.count(), 1)

    def test_create_item_with_project_scope(self):
        data = {"category_id": self.cat1.pk, "title": "Scoped Item", "project_scope_id": self.scope.pk, "order": 1}
        response = self.client.post(reverse("expertisecategory-items", args=[self.cat1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item = ExpertiseItem.objects.get(title="Scoped Item")
        self.assertEqual(item.project_scope_id, self.scope.pk)

    def test_create_item_validation_error(self):
        data = {"category_id": self.cat1.pk, "project_scope_id": 9999}
        response = self.client.post(reverse("expertisecategory-items", args=[self.cat1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_item(self):
        item = ExpertiseItem.objects.create(category=self.cat1, title="Item1")
        response = self.client.get(reverse("expertisecategory-item-detail", args=[self.cat1.pk, item.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Item1")

    def test_update_item(self):
        item = ExpertiseItem.objects.create(category=self.cat1, title="Old")
        data = {"category_id": self.cat1.pk, "title": "Updated"}
        response = self.client.put(
            reverse("expertisecategory-item-detail", args=[self.cat1.pk, item.pk]),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        item = ExpertiseItem.objects.create(category=self.cat1, title="ToDelete")
        response = self.client.delete(reverse("expertisecategory-item-detail", args=[self.cat1.pk, item.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExpertiseItem.objects.count(), 0)

    def test_retrieve_item_not_found(self):
        response = self.client.get(reverse("expertisecategory-item-detail", args=[self.cat1.pk, 9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SectorViewSetTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.s1 = ServiceSector.objects.create(title="Hydropower", order=1)
        ServiceSector.objects.create(title="Solar", order=2)

    def test_list(self):
        response = self.client.get(reverse("servicesector-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        data = {"title": "Wind", "order": 3}
        response = self.client.post(reverse("servicesector-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceSector.objects.count(), 3)

    def test_retrieve(self):
        response = self.client.get(reverse("servicesector-detail", args=[self.s1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Hydropower")

    def test_update(self):
        data = {"title": "Updated", "order": 1}
        response = self.client.put(reverse("servicesector-detail", args=[self.s1.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("servicesector-detail", args=[self.s1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceSector.objects.count(), 1)
