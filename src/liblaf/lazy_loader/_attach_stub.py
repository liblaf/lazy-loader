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
    """Create module hooks from a sibling stub file.

    Call this from a package `__init__.py` and assign the returned values to
    `__getattr__`, `__dir__`, and `__all__`. The function reads the adjacent
    `.pyi` file, parses its explicit import statements into a [LazyLoader]
    [liblaf.lazy_loader.LazyLoader], and optionally resolves every export at
    import time when `EAGER_IMPORT` is enabled.

    Args:
        name: Module name, typically `__name__`.
        package: Package name used to resolve relative imports, typically
            `__package__`.
        file: Path to the module file whose sibling `.pyi` file declares the
            lazy exports, typically `__file__`.

    Returns:
        A tuple containing `__getattr__`, `__dir__`, and `__all__` in that
        order.

    Raises:
        FileNotFoundError: If the sibling `.pyi` file does not exist.
        SyntaxError: If the sibling stub cannot be parsed as Python.
        ValueError: If `EAGER_IMPORT` is not a valid boolean string or the stub
            uses an unsupported construct such as a wildcard import.
        ImportError: If eager loading is enabled and one of the declared
            imports cannot be resolved.
    """
    file: Path = Path(file)
    stub_file: Path = file.with_suffix(".pyi")
    node: ast.Module = ast.parse(stub_file.read_text())
    visitor: StubVisitor = StubVisitor()
    visitor.visit(node)
    loader: LazyLoader = visitor.finish(name=name, package=package)
    if env_bool("EAGER_IMPORT", False):  # noqa: FBT003
        for attr_name in loader.getters:
            loader.__getattr__(attr_name)
    return loader.__getattr__, loader.__dir__, loader.__all__
