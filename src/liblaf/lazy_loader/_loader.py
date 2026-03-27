import dataclasses
import functools
import sys
import types
from typing import Any

from ._getter import Getter, GetterContext


@dataclasses.dataclass(frozen=True)
class LazyLoader:
    name: str
    package: str | None
    exports: list[str] | None
    getters: dict[str, Getter]

    @functools.cached_property
    def __all__(self) -> list[str]:
        if self.exports is not None:
            return self.exports
        return list(self.getters.keys())

    def __dir__(self) -> list[str]:
        return sorted(set().union(vars(self.module), self.__all__))

    def __getattr__(self, name: str) -> Any:
        if name not in self.getters:
            msg: str = f"module '{self.name}' has no attribute '{name}'"
            raise AttributeError(msg, name=name, obj=self.module)
        getter: Getter = self.getters[name]
        value: Any = getter.get(self.context)
        setattr(self.module, name, value)
        return value

    @functools.cached_property
    def context(self) -> GetterContext:
        return GetterContext(module=self.name, package=self.package)

    @functools.cached_property
    def module(self) -> types.ModuleType:
        return sys.modules[self.name]
