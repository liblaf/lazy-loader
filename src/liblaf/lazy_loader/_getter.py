import abc
import dataclasses
import importlib
import types
from typing import Any, override

from ._utils import MISSING


@dataclasses.dataclass(frozen=True, slots=True)
class GetterContext:
    """Carry module metadata needed to resolve a lazy export."""

    """Fully qualified module name receiving the lazy attributes."""
    module: str
    """Package anchor used for relative imports."""
    package: str | None


@dataclasses.dataclass(frozen=True, slots=True)
class Getter(abc.ABC):
    """Define how one exported name is resolved from a stub entry."""

    @property
    @abc.abstractmethod
    def attr_name(self) -> str:
        """Return the attribute name exposed on the target module."""

    @abc.abstractmethod
    def get(self, ctx: GetterContext) -> Any:
        """Resolve the exported value for the given module context."""


@dataclasses.dataclass(frozen=True, slots=True)
class GetterImport(Getter):
    """Resolve an `import ...` statement from the stub file.

    An aliased import exposes the alias directly. Without an alias, the getter
    follows Python import semantics and exposes the top-level module name.
    """

    """Module path written in the stub import statement."""
    name: str
    """Optional alias exposed on the lazily loaded module."""
    asname: str | None

    @property
    @override
    def attr_name(self) -> str:
        if self.asname:
            return self.asname
        return self.name.split(".", 1)[0]

    @override
    def get(self, ctx: GetterContext) -> Any:
        if self.asname:
            return importlib.import_module(self.name, package=ctx.package)
        importlib.import_module(self.name, package=ctx.package)
        asname: str = self.name.split(".", 1)[0]
        return importlib.import_module(asname, package=ctx.package)


@dataclasses.dataclass(frozen=True, slots=True)
class GetterImportFrom(Getter):
    """Resolve a `from ... import ...` statement from the stub file.

    This getter supports both absolute imports and relative imports. When a
    direct attribute lookup would recurse back into the lazily loaded module, it
    falls back to importing the submodule itself.
    """

    """Module part of the import-from statement, if present."""
    module: str | None
    """Imported attribute or submodule name."""
    name: str
    """Optional alias exposed on the lazily loaded module."""
    asname: str | None
    """Relative import depth encoded by the stub AST node."""
    level: int

    @property
    @override
    def attr_name(self) -> str:
        return self.asname or self.name

    @override
    def get(self, ctx: GetterContext) -> Any:
        module_name: str = "." * self.level
        if self.module:
            module_name += self.module
        module: types.ModuleType = importlib.import_module(
            module_name, package=ctx.package
        )
        if module.__name__ != ctx.module:  # avoid recursion
            value: Any = getattr(module, self.name, MISSING)
            if value is not MISSING:
                return value
        module_name += f".{self.name}" if self.module else self.name
        return importlib.import_module(module_name, package=ctx.package)
