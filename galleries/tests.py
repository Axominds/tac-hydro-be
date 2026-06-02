from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from galleries.models import GalleryCategory, GalleryImage, GallerySubcategory
from galleries.serializers.gallery_category import (
    GalleryCategoryCreateSerializer,
    GalleryCategoryDetailSerializer,
    GalleryCategoryListSerializer,
    GalleryCategoryUpdateSerializer,
)
from galleries.serializers.gallery_subcategory import (
    GallerySubcategoryCreateSerializer,
    GallerySubcategoryDetailSerializer,
    GallerySubcategoryListSerializer,
    GallerySubcategoryUpdateSerializer,
)
from galleries.serializers.gallery_image import (
    GalleryImageCreateSerializer,
    GalleryImageDetailSerializer,
    GalleryImageListSerializer,
    GalleryImageUpdateSerializer,
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

class GalleryCategoryModelTests(TestCase):
    def test_create(self):
        cat = GalleryCategory.objects.create(name="Projects", order=1)
        self.assertEqual(str(cat), "Projects")


class GallerySubcategoryModelTests(TestCase):
    def setUp(self):
        self.cat = GalleryCategory.objects.create(name="Gallery")

    def test_create(self):
        sub = GallerySubcategory.objects.create(category=self.cat, name="Sub", order=1)
        self.assertEqual(str(sub), "Sub")

    def test_cascade_on_category_delete(self):
        GallerySubcategory.objects.create(category=self.cat, name="Sub")
        self.assertEqual(GallerySubcategory.objects.count(), 1)
        self.cat.delete()
        self.assertEqual(GallerySubcategory.objects.count(), 0)


class GalleryImageModelTests(TestCase):
    def setUp(self):
        self.cat = GalleryCategory.objects.create(name="Gallery")
        self.sub = GallerySubcategory.objects.create(category=self.cat, name="Sub")

    def test_create(self):
        img = GalleryImage.objects.create(
            gallery_subcategory=self.sub,
            image=SimpleUploadedFile("img.jpg", b"data"),
            order=1,
        )
        self.assertIn("Sub", str(img))

    def test_cascade_on_subcategory_delete(self):
        GalleryImage.objects.create(gallery_subcategory=self.sub, image=SimpleUploadedFile("img.jpg", b"d"))
        self.assertEqual(GalleryImage.objects.count(), 1)
        self.sub.delete()
        self.assertEqual(GalleryImage.objects.count(), 0)


# ─── Serializer Tests ──────────────────────────────────────────────

class GalleryCategorySerializerTests(TestCase):
    def test_create_serializer_valid(self):
        data = {"name": "New Category", "order": 1}
        serializer = GalleryCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_fields(self):
        cat = GalleryCategory.objects.create(name="Test")
        serializer = GalleryCategoryListSerializer(cat)
        self.assertIn("id", serializer.data)
        self.assertIn("name", serializer.data)
        self.assertIn("order", serializer.data)


class GallerySubcategorySerializerTests(TestCase):
    def setUp(self):
        self.cat = GalleryCategory.objects.create(name="Gallery")

    def test_create_serializer_valid(self):
        data = {"category_id": self.cat.pk, "name": "Sub", "order": 1}
        serializer = GallerySubcategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_invalid_category(self):
        data = {"category_id": 9999, "name": "Sub"}
        serializer = GallerySubcategoryCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category_id", serializer.errors)

    def test_list_serializer_fields(self):
        sub = GallerySubcategory.objects.create(category=self.cat, name="Sub")
        serializer = GallerySubcategoryListSerializer(sub)
        self.assertIn("id", serializer.data)
        self.assertIn("category_id", serializer.data)
        self.assertIn("name", serializer.data)


class GalleryImageSerializerTests(TestCase):
    def setUp(self):
        self.cat = GalleryCategory.objects.create(name="Gallery")
        self.sub = GallerySubcategory.objects.create(category=self.cat, name="Sub")

    def test_create_serializer_valid(self):
        data = {"order": 1, "image": SimpleUploadedFile("img.jpg", b"data")}
        serializer = GalleryImageCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_list_serializer_fields(self):
        img = GalleryImage.objects.create(gallery_subcategory=self.sub, image=SimpleUploadedFile("img.jpg", b"d"))
        serializer = GalleryImageListSerializer(img)
        self.assertIn("id", serializer.data)
        self.assertIn("image", serializer.data)
        self.assertIn("gallery_subcategory_id", serializer.data)
        self.assertIn("order", serializer.data)


# ─── View Tests ────────────────────────────────────────────────────

class GalleryViewCategoryTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.c1 = GalleryCategory.objects.create(name="Projects", order=1)
        self.c2 = GalleryCategory.objects.create(name="Events", order=2)

    def test_list(self):
        response = self.client.get(reverse("gallery-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create(self):
        response = self.client.post(reverse("gallery-list"), {"name": "New"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GalleryCategory.objects.count(), 3)

    def test_retrieve(self):
        response = self.client.get(reverse("gallery-detail", args=[self.c1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Projects")

    def test_update(self):
        response = self.client.put(
            reverse("gallery-detail", args=[self.c1.pk]),
            {"name": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse("gallery-detail", args=[self.c1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_read_allowed(self):
        client = APIClient()
        response = client.get(reverse("gallery-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_write_denied(self):
        client = APIClient()
        response = client.post(reverse("gallery-list"), {"name": "T"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GallerySubcategoryNestedTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.cat = GalleryCategory.objects.create(name="Gallery")
        self.sub1 = GallerySubcategory.objects.create(category=self.cat, name="Interior", order=1)
        GallerySubcategory.objects.create(category=self.cat, name="Exterior", order=2)

    def test_list_subcategories(self):
        response = self.client.get(reverse("gallery-subcategories", args=[self.cat.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_subcategory(self):
        data = {"name": "New Sub", "order": 3}
        response = self.client.post(reverse("gallery-subcategories", args=[self.cat.pk]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GallerySubcategory.objects.count(), 3)

    def test_retrieve_subcategory(self):
        url = reverse("gallery-subcategory-detail", args=[self.cat.pk, self.sub1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Interior")

    def test_update_subcategory(self):
        url = reverse("gallery-subcategory-detail", args=[self.cat.pk, self.sub1.pk])
        data = {"category_id": self.cat.pk, "name": "Updated"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subcategory(self):
        url = reverse("gallery-subcategory-detail", args=[self.cat.pk, self.sub1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GallerySubcategory.objects.count(), 1)

    def test_subcategory_not_found(self):
        url = reverse("gallery-subcategory-detail", args=[self.cat.pk, 9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GalleryImageNestedTests(TestCase):
    def setUp(self):
        self.client, self.user = create_authenticated_client()
        self.cat = GalleryCategory.objects.create(name="Gallery")
        self.sub = GallerySubcategory.objects.create(category=self.cat, name="Sub")
        self.img1 = GalleryImage.objects.create(
            gallery_subcategory=self.sub,
            image=SimpleUploadedFile("img1.jpg", b"data1"),
            order=1,
        )
        GalleryImage.objects.create(
            gallery_subcategory=self.sub,
            image=SimpleUploadedFile("img2.jpg", b"data2"),
            order=2,
        )

    def test_list_images(self):
        response = self.client.get(reverse("gallery-images", args=[self.cat.pk, self.sub.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_image(self):
        data = {"order": 3, "image": SimpleUploadedFile("img3.jpg", b"data3")}
        url = reverse("gallery-images", args=[self.cat.pk, self.sub.pk])
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GalleryImage.objects.count(), 3)

    def test_retrieve_image(self):
        url = reverse("gallery-image-detail", args=[self.cat.pk, self.sub.pk, self.img1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order"], 1)

    def test_update_image(self):
        url = reverse("gallery-image-detail", args=[self.cat.pk, self.sub.pk, self.img1.pk])
        data = {"order": 5, "image": SimpleUploadedFile("updated.jpg", b"new")}
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_image(self):
        url = reverse("gallery-image-detail", args=[self.cat.pk, self.sub.pk, self.img1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GalleryImage.objects.count(), 1)

    def test_image_not_found(self):
        url = reverse("gallery-image-detail", args=[self.cat.pk, self.sub.pk, 9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subcategory_not_found(self):
        url = reverse("gallery-images", args=[self.cat.pk, 9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_images(self):
        response = self.client.get(reverse("gallery-category-images", args=[self.cat.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_all_images(self):
        response = self.client.get(reverse("gallery-all-images"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
