from __future__ import annotations

import contextlib
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import IdentityFunction


_ENV_BOOL_FALSY: set[str] = {
    "0",
    "F",
    "FALSE",
    "False",
    "N",
    "NO",
    "No",
    "OFF",
    "Off",
    "f",
    "false",
    "n",
    "no",
    "off",
}
_ENV_BOOL_TRUTHY: set[str] = {
    "1",
    "ON",
    "On",
    "T",
    "TRUE",
    "True",
    "Y",
    "YES",
    "Yes",
    "on",
    "t",
    "true",
    "y",
    "yes",
}


def env_bool(name: str, default: bool = False) -> bool:  # noqa: FBT001, FBT002
    value: str | None = os.getenv(name)
    if value is None:
        return default
    if value in _ENV_BOOL_TRUTHY:
        return True
    if value in _ENV_BOOL_FALSY:
        return False
    msg: str = f"Environment variable {name!r} invalid: Not a valid boolean."
    raise ValueError(msg)


def export(module: str) -> IdentityFunction:
    def decorator[F](obj: F) -> F:
        if hasattr(obj, "__module__"):
            with contextlib.suppress(Exception):
                obj.__module__ = module
        return obj

    return decorator


def normalize_qualname[T](obj: T) -> T:
    if hasattr(obj, "__name__") and hasattr(obj, "__qualname__"):
        with contextlib.suppress(Exception):
            obj.__qualname__ = obj.__name__  # ty:ignore[invalid-assignment]
    return obj
