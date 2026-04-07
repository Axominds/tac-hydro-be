from typing import Any, Type

from rest_framework import viewsets
from rest_framework.serializers import Serializer


class ModelViewSetWithFieldSets(viewsets.ModelViewSet):
    list_serializer_class: Type[Serializer] | None = None
    create_serializer_class: Type[Serializer] | None = None
    update_serializer_class: Type[Serializer] | None = None
    partial_update_serializer_class: Type[Serializer] | None = None

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list" and self.list_serializer_class:
            return self.list_serializer_class
        if self.action == "create" and self.create_serializer_class:
            return self.create_serializer_class
        if self.action == "update" and self.update_serializer_class:
            return self.update_serializer_class
        if self.action == "partial_update" and self.partial_update_serializer_class:
            return self.partial_update_serializer_class
        return super().get_serializer_class()
