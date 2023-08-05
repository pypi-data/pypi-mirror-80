import importlib
from functools import wraps
from pathlib import Path


def import_all(filename, name):
    for path in Path(filename).resolve().parent.glob("*.py"):
        if path.stem != "__init__":
            importlib.import_module(f".{path.stem}", name)


def requires_all_imports(import_all):
    def wrapper(fn):
        all_imported = False

        @wraps(fn)
        def wrapped(*args, **kwargs):
            nonlocal all_imported

            if not all_imported:
                import_all()
                all_imported = True

            return fn(*args, **kwargs)

        return wrapped

    return wrapper


def wrap(val):
    if isinstance(val, (list, tuple)):
        return val
    else:
        return (val,)
