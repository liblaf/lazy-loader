import dataclasses
import functools
import sys
import types
from typing import Any

from ._getter import Getter, GetterContext


@dataclasses.dataclass(frozen=True)
class LazyLoader:
    """Resolve stub-declared exports on first attribute access.

    The loader backs the tuple returned by
    [attach_stub][liblaf.lazy_loader.attach_stub]. It keeps the parsed getter
    objects, exposes a module-friendly `__dir__` and `__all__`, and caches each
    resolved value onto the target module after the first lookup.
    """

    """Fully qualified name of the module being populated."""
    name: str
    """Package anchor used for relative imports."""
    package: str | None
    """Export names declared by `__all__` in the stub, if present."""
    exports: list[str] | None
    """Mapping from exported attribute names to getter objects."""
    getters: dict[str, Getter]

    @functools.cached_property
    def __all__(self) -> list[str]:
        """Return exported names for module `__all__`."""
        if self.exports is not None:
            return self.exports
        return list(self.getters.keys())

    def __dir__(self) -> list[str]:
        """List declared exports together with materialized module attributes."""
        return sorted(set().union(vars(self.module), self.__all__))

    def __getattr__(self, name: str) -> Any:
        """Import and cache one declared export.

        Args:
            name: Exported attribute name requested from the module.

        Returns:
            The resolved module, function, class, or other imported object.

        Raises:
            AttributeError: If `name` is not declared by the stub.
            ImportError: If resolving the declared import fails.
        """
        if name not in self.getters:
            msg: str = f"module '{self.name}' has no attribute '{name}'"
            raise AttributeError(msg, name=name, obj=self.module)
        getter: Getter = self.getters[name]
        value: Any = getter.get(self.context)
        setattr(self.module, name, value)
        return value

    @functools.cached_property
    def context(self) -> GetterContext:
        """Return import context shared by all getters."""
        return GetterContext(module=self.name, package=self.package)

    @functools.cached_property
    def module(self) -> types.ModuleType:
        """Return the target module object from `sys.modules`."""
        return sys.modules[self.name]
