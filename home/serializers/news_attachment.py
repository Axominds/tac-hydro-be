from rest_framework import serializers

from home.models import NewsAttachment


class NewsAttachmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        fields = ["id", "news_id", "title"]


class NewsAttachmentDetailSerializer(NewsAttachmentListSerializer):
    class Meta(NewsAttachmentListSerializer.Meta):
        fields = ["id", "news_id", "file", "title"]


class NewsAttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        fields = ["news_id", "title"]


class NewsAttachmentUpdateSerializer(NewsAttachmentCreateSerializer):
    class Meta(NewsAttachmentCreateSerializer.Meta):
        pass
