from django_bolt.views import ModelViewSet

from about_us.models import CorePrinciple
from about_us.serializers.core_principle import (
    CorePrincipleDetailSerializer,
    CorePrincipleListSerializer,
)


class CorePrincipleViewSet(ModelViewSet):
    queryset = CorePrinciple.objects.all()
    serializer_class = CorePrincipleDetailSerializer
    list_serializer_class = CorePrincipleListSerializer
