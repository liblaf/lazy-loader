import ast
import sys
import types
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ._loader import Loader, LoaderContext
from ._utils import env_bool, export, normalize_qualname
from ._visitor import StubVisitor

type GetAttr = Callable[[str], Any]
type Dir = Callable[[], list[str]]
type All = list[str]


def attach_stub(
    module: str, package: str | None, file: str
) -> tuple[GetAttr, Dir, All]:
    loaders: dict[str, Loader] = _parse_stub(file)
    mod: types.ModuleType = sys.modules[module]
    ctx: LoaderContext = LoaderContext(module, package)
    __all__: list[str] = sorted(loaders.keys())

    @export(module)
    @normalize_qualname
    def __getattr__(name: str) -> Any:  # noqa: N807
        if name in loaders:
            loader: Loader = loaders[name]
            value: Any = loader.load(ctx)
            setattr(mod, name, value)
            return value
        msg: str = f"module '{module}' has no attribute '{name}'"
        raise AttributeError(msg, name=name, obj=mod)

    @export(module)
    @normalize_qualname
    def __dir__() -> list[str]:  # noqa: N807
        return __all__.copy()

    if env_bool("EAGER_IMPORT", False):  # noqa: FBT003
        for attr_name in __all__:
            __getattr__(attr_name)

    return __getattr__, __dir__, __all__


def _parse_stub(file: str) -> dict[str, Loader]:
    file: Path = Path(file)
    stub_file: Path = file.with_suffix(".pyi")
    node: ast.Module = ast.parse(stub_file.read_text())
    visitor: StubVisitor = StubVisitor()
    visitor.visit(node)
    return visitor.loaders
