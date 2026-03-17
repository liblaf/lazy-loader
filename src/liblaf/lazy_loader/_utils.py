from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import IdentityFunction


def export(module: str) -> IdentityFunction:
    def decorator[F](obj: F) -> F:
        if hasattr(obj, "__module__"):
            with contextlib.suppress(AttributeError):
                obj.__module__ = module
        if hasattr(obj, "__name__") and hasattr(obj, "__qualname__"):
            with contextlib.suppress(AttributeError):
                obj.__qualname__ = obj.__name__  # ty:ignore[invalid-assignment]
        return obj

    return decorator
