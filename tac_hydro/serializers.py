from typing import Any, ClassVar

from rest_framework import serializers


class FieldSetsMixin:
    field_sets: ClassVar[dict[str, list[str]]] = {}

    @classmethod
    def fields(cls, field_set_name: str) -> type[serializers.Serializer]:
        if field_set_name not in cls.field_sets:
            raise ValueError(f"Unknown field_set: {field_set_name}. Available: {list(cls.field_sets.keys())}")

        field_names = cls.field_sets[field_set_name]

        class FieldSetSerializer(cls):
            class Meta:
                pass

        for attr_name in dir(FieldSetSerializer):
            if not attr_name.startswith("_"):
                try:
                    delattr(FieldSetSerializer, attr_name)
                except TypeError, AttributeError:
                    pass

        FieldSetSerializer.__name__ = f"{cls.__name__}{field_set_name.title().replace('_', '')}Serializer"
        FieldSetSerializer.__qualname__ = f"{cls.__qualname__}{field_set_name.title().replace('_', '')}Serializer"

        for field_name in field_names:
            if field_name in cls._declared_fields:
                FieldSetSerializer._declared_fields[field_name] = cls._declared_fields[field_name]
            elif hasattr(cls.Meta, "model"):
                pass
            else:
                pass

        return FieldSetSerializer


def computed_field(func):
    return serializers.SerializerMethodField()(func)


class ModelSerializerWithFieldSets(FieldSetsMixin, serializers.ModelSerializer):
    pass
