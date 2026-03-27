import ast
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ._loader import LazyLoader
from ._utils import env_bool
from ._visitor import StubVisitor

type GetAttr = Callable[[str], Any]
type Dir = Callable[[], list[str]]
type All = list[str]


def attach_stub(name: str, package: str | None, file: str) -> tuple[GetAttr, Dir, All]:
    file: Path = Path(file)
    stub_file: Path = file.with_suffix(".pyi")
    node: ast.Module = ast.parse(stub_file.read_text())
    visitor: StubVisitor = StubVisitor()
    visitor.visit(node)
    loader: LazyLoader = visitor.finish(name=name, package=package)
    if env_bool("EAGER_IMPORT", False):  # noqa: FBT003
        for attr_name in loader.__all__:
            loader.__getattr__(attr_name)
    return loader.__getattr__, loader.__dir__, loader.__all__
