from rest_framework import viewsets

from home.models import NewsCategory
from home.serializers.news_category import (
    NewsCategoryCreateSerializer,
    NewsCategoryDetailSerializer,
    NewsCategoryListSerializer,
    NewsCategoryUpdateSerializer,
)


class NewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategoryDetailSerializer
    list_serializer_class = NewsCategoryListSerializer
    create_serializer_class = NewsCategoryCreateSerializer
    update_serializer_class = NewsCategoryUpdateSerializer
    partial_update_serializer_class = NewsCategoryUpdateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()
