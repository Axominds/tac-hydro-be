from pathlib import Path

from django.conf import settings
from django_bolt.serializers import Serializer as BaseSerializer

MEDIA_ROOT = Path(settings.MEDIA_ROOT)

_serializer_instances: dict[int, object] = {}


def _patch_from_model():
    original = BaseSerializer.from_model

    def from_model(cls, obj, *, _depth=0, max_depth=10, **kwargs):
        instance = original.__func__(cls, obj, _depth=_depth, max_depth=max_depth, **kwargs)
        _serializer_instances[id(instance)] = obj
        return instance

    BaseSerializer.from_model = classmethod(from_model)


_patch_from_model()
