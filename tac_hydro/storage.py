import functools
import hashlib
import uuid
from pathlib import Path

from django.db.models import FileField


def _hashed_upload_to(instance, filename, prefix):
    ext = Path(filename).suffix.lower()
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            f = getattr(instance, field.name)
            if f and hasattr(f, "file") and f.file:
                f.file.seek(0)
                h = hashlib.md5()
                for chunk in f.file.chunks():
                    h.update(chunk)
                f.file.seek(0)
                return f"{prefix}/{h.hexdigest()}{ext}"
    return f"{prefix}/{uuid.uuid4().hex}{ext}"


def hashed_upload_to(prefix: str):
    return functools.partial(_hashed_upload_to, prefix=prefix)
