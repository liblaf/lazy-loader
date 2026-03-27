import abc
import dataclasses
import importlib
import types
from typing import Any, override

from ._utils import MISSING


@dataclasses.dataclass(frozen=True, slots=True)
class GetterContext:
    module: str
    package: str | None


@dataclasses.dataclass(frozen=True, slots=True)
class Getter(abc.ABC):
    @property
    @abc.abstractmethod
    def attr_name(self) -> str: ...

    @abc.abstractmethod
    def get(self, ctx: GetterContext) -> Any: ...


@dataclasses.dataclass(frozen=True, slots=True)
class GetterImport(Getter):
    name: str
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
    module: str | None
    name: str
    asname: str | None
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
