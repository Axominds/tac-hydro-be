import os
import django
import pkgutil
import inspect
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tac_hydro.settings")
django.setup()

from django.apps import apps
from django_bolt.serializers import Serializer

def check_serializers():
    for app_config in apps.get_app_configs():
        if not app_config.path.startswith(str(Path.cwd())):
            continue
        
        serializer_dir = Path(app_config.path) / 'serializers'
        if not serializer_dir.exists():
            continue
            
        import importlib
        models_dict = {m.__name__: m for m in app_config.get_models()}
        
        for file in serializer_dir.glob('**/*.py'):
            if file.name == '__init__.py': continue
            
            module_name = file.relative_to(Path.cwd()).with_suffix('').as_posix().replace('/', '.')
            try:
                mod = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, Serializer) and obj is not Serializer:
                        model_name = name.replace('Serializer', '')
                        if model_name in models_dict:
                            check_model_serializer(models_dict[model_name], obj)
            except Exception as e:
                pass

def check_model_serializer(model, serializer_class):
    create_fields = set(serializer_class.Config.field_sets.get("create", []))
    update_fields = set(serializer_class.Config.field_sets.get("update", []))

    model_fields = []
    for f in model._meta.get_fields():
        from django.db.models import fields
        if f.auto_created or not getattr(f, 'editable', True):
            continue
        if isinstance(f, fields.files.FileField):
            continue
        
        model_fields.append(f.name)
        if f.is_relation and f.many_to_one:
            model_fields.append(f.attname)

    missing = []
    for mf in model_fields:
        if mf not in create_fields and not (mf.endswith('_id') and mf[:-3] in create_fields) and not (mf + '_id' in create_fields) and mf not in ['id']:
            missing.append(mf)
            
    if missing:
        print(f"Missing in CREATE for {serializer_class.__name__}: {missing}")

if __name__ == "__main__":
    check_serializers()
