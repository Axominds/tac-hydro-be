from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from services.models import ExpertiseCategory, ExpertiseItem
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


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = ExpertiseCategory.objects.all()
    serializer_class = ExpertiseCategoryDetailSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ExpertiseCategoryListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ExpertiseCategoryCreateSerializer
        return super().get_serializer_class()

    @action(detail=True, url_path="items")
    def items(self, request: Request, pk=None):
        category = self.get_object()
        if request.method == "GET":
            items = category.items.all()
            serializer = ExpertiseItemListSerializer(items, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = ExpertiseItemCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(category=category)
            return Response(ExpertiseItemDetailSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_path="items/(?P<item_id>[^/.]+)", methods=["get", "put", "patch", "delete"])
    def item_detail(self, request: Request, pk=None, item_id=None):
        category = self.get_object()
        try:
            item = category.items.get(pk=item_id)
        except ExpertiseItem.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = ExpertiseItemDetailSerializer(item)
            return Response(serializer.data)
        elif request.method in ["PUT", "PATCH"]:
            serializer = ExpertiseItemUpdateSerializer(item, data=request.data, partial=request.method == "PATCH")
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(ExpertiseItemDetailSerializer(item).data)
        else:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
