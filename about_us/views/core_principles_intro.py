from django_bolt.views import ModelViewSet

from about_us.models import CorePrinciplesIntro
from about_us.serializers.core_principles_intro import (
    CorePrinciplesIntroDetailSerializer,
    CorePrinciplesIntroListSerializer,
)


class CorePrinciplesIntroViewSet(ModelViewSet):
    queryset = CorePrinciplesIntro.objects.all()
    serializer_class = CorePrinciplesIntroDetailSerializer
    list_serializer_class = CorePrinciplesIntroListSerializer
