import builtins

from django_bolt import PageNumberPagination, paginate
from django_bolt.views import ModelViewSet

from home.models import News
from home.serializers.news import (
    NewsListSerializer,
    NewsRetrieveSerializer,
)


class ArticlePagination(PageNumberPagination):
    page_size = 3
    max_page_size = 100
    page_size_query_param = "page_size"  # Allow client to customize


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsRetrieveSerializer
    list_serializer_class = NewsListSerializer

    # retrieve API at the moment required explicit override in django-bolt
    async def retrieve(self, request, pk: int):
        return await super().retrieve(request, pk=pk)

    @paginate(ArticlePagination)
    async def list(self, request, news_category_id: int | None = None) -> builtins.list[NewsListSerializer]:
        super().list(request)
        qs = await self.get_queryset()
        if news_category_id:
            qs = qs.filter(news_category_id=news_category_id)
        qs = await self.filter_queryset(qs)  # Apply filtering (still lazy)
        return qs
