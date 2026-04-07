from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from home.models import News
from home.serializers.news import (
    NewsCreateSerializer,
    NewsListSerializer,
    NewsRetrieveSerializer,
    NewsUpdateSerializer,
)


class ArticlePagination(PageNumberPagination):
    page_size = 3
    max_page_size = 100
    page_size_query_param = "page_size"


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsRetrieveSerializer
    list_serializer_class = NewsListSerializer
    create_serializer_class = NewsCreateSerializer
    update_serializer_class = NewsUpdateSerializer
    partial_update_serializer_class = NewsUpdateSerializer
    pagination_class = ArticlePagination

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        if self.action in ["create", "update", "partial_update"]:
            return self.create_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = News.objects.all()
        news_category_id = self.request.query_params.get("news_category_id")
        if news_category_id:
            queryset = queryset.filter(news_category_id=news_category_id)
        return queryset
