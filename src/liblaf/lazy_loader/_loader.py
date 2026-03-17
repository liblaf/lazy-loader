import abc
import contextlib
import dataclasses
import importlib
import types
from typing import Any, override


@dataclasses.dataclass(slots=True)
class LoaderContext:
    module: str
    package: str | None


@dataclasses.dataclass(slots=True)
class Loader(abc.ABC):
    @property
    @abc.abstractmethod
    def attr_name(self) -> str: ...

    @abc.abstractmethod
    def load(self, ctx: LoaderContext) -> Any: ...


@dataclasses.dataclass(slots=True)
class LoaderImport(Loader):
    name: str
    asname: str | None

    @property
    @override
    def attr_name(self) -> str:
        if self.asname:
            return self.asname
        return self.name.split(".", 1)[0]

    @override
    def load(self, ctx: LoaderContext) -> Any:
        if self.asname:
            return importlib.import_module(self.name, package=ctx.package)
        importlib.import_module(self.name, package=ctx.package)
        return importlib.import_module(self.name.split(".", 1)[0], package=ctx.package)


@dataclasses.dataclass(slots=True)
class LoaderImportFrom(Loader):
    module: str | None
    name: str
    asname: str | None
    level: int

    @property
    @override
    def attr_name(self) -> str:
        return self.asname or self.name

    @override
    def load(self, ctx: LoaderContext) -> Any:
        module_name: str = "." * self.level
        if self.module:
            module_name += self.module
        module: types.ModuleType = importlib.import_module(
            module_name, package=ctx.package
        )
        if module.__name__ != ctx.module:  # avoid recursion
            with contextlib.suppress(AttributeError):
                return getattr(module, self.name)
        module_name += f".{self.name}" if self.module else self.name
        return importlib.import_module(module_name, package=ctx.package)
