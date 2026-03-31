"""Stub-driven lazy exports for package modules.

Use [attach_stub][liblaf.lazy_loader.attach_stub] in a package `__init__.py` and
declare the exported imports in the adjacent `.pyi` file. The runtime loader
supports both package-relative imports and absolute imports while keeping the
public surface area small.
"""

from ._attach_stub import attach_stub
from ._getter import Getter, GetterContext, GetterImport, GetterImportFrom
from ._loader import LazyLoader
from ._utils import env_bool
from ._version import __commit_id__, __version__, __version_tuple__
from ._visitor import StubVisitor

__all__ = [
    "Getter",
    "GetterContext",
    "GetterImport",
    "GetterImportFrom",
    "LazyLoader",
    "StubVisitor",
    "__commit_id__",
    "__version__",
    "__version_tuple__",
    "attach_stub",
    "env_bool",
]
