<div align="center" markdown>

![lazy-loader](https://socialify.git.ci/liblaf/lazy-loader/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Transparent&pulls=1&stargazers=1&theme=Auto)

**[Explore the docs »](https://liblaf-lazy-loader.readthedocs.io/)**

[![codecov](https://codecov.io/gh/liblaf/lazy-loader/graph/badge.svg)](https://codecov.io/gh/liblaf/lazy-loader)
[![Docs](https://github.com/liblaf/lazy-loader/actions/workflows/python-docs.yaml/badge.svg)](https://github.com/liblaf/lazy-loader/actions/workflows/python-docs.yaml)
[![MegaLinter](https://github.com/liblaf/lazy-loader/actions/workflows/shared-mega-linter.yaml/badge.svg)](https://github.com/liblaf/lazy-loader/actions/workflows/shared-mega-linter.yaml)
[![Tests](https://github.com/liblaf/lazy-loader/actions/workflows/python-test.yaml/badge.svg)](https://github.com/liblaf/lazy-loader/actions/workflows/python-test.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/liblaf/lazy-loader/main.svg)](https://results.pre-commit.ci/latest/github/liblaf/lazy-loader/main)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liblaf-lazy-loader?logo=Python&label=Python)](https://pypi.org/project/liblaf-lazy-loader)
[![PyPI - Version](https://img.shields.io/pypi/v/liblaf-lazy-loader?logo=PyPI&label=PyPI)](https://pypi.org/project/liblaf-lazy-loader)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

[Changelog](https://github.com/liblaf/lazy-loader/blob/main/CHANGELOG.md) · [Report Bug](https://github.com/liblaf/lazy-loader/issues) · [Request Feature](https://github.com/liblaf/lazy-loader/issues)

![Rule](https://cdn.jsdelivr.net/gh/andreasbm/readme/assets/lines/rainbow.png)

</div>

`liblaf-lazy-loader` lets Python packages expose stub-driven lazy exports with both absolute imports and package-relative imports.

## ✨ Features

- 💤 **Stub-driven lazy imports:** Parse a sibling `.pyi` file and turn its `import` and `from ... import ...` statements into on-demand attribute loaders.
- 📦 **Module-friendly exports:** Preserve `__all__` and enrich `dir()` so interactive use and star exports stay aligned with the stub definition.
- 🔁 **Absolute and relative import support:** Handle both local package imports and external modules, including aliased imports.
- ⚡ **Optional eager mode:** Set `EAGER_IMPORT=1` to resolve every declared export at import time when startup indirection is not wanted.
- 🧭 **Typed, tiny surface area:** Ship as a typed package with no runtime dependencies and a small public API centered on `attach_stub` and `LazyLoader`.
- 🔄 **Drop-in `attach_stub` call:** Support the familiar `attach_stub(__name__, __file__)` signature, with an optional trailing `__package__` override when needed.

## 📦 Installation

> [!NOTE]
> `liblaf-lazy-loader` requires Python 3.12 or newer.

```bash
uv add liblaf-lazy-loader
```

## 🚀 Quick Start

In `mypkg/__init__.py`, wire the package up once:

```python
from liblaf.lazy_loader import attach_stub

__getattr__, __dir__, __all__ = attach_stub(__name__, __file__)
```

If you need to pass an explicit package anchor, use the optional third argument:

```python
__getattr__, __dir__, __all__ = attach_stub(__name__, __file__, __package__)
```

In the sibling `mypkg/__init__.pyi`, declare the exports you want to load lazily:

```python
from . import cli
from ._config import Settings
from ._factory import make_settings
from rich import get_console
import rich.console as rich_console

__all__ = ["Settings", "cli", "get_console", "make_settings", "rich_console"]
```

With that wiring in place, `Settings`, `cli`, `make_settings`, `get_console`, and `rich_console` are imported only when first accessed. When the third argument is omitted entirely, `attach_stub` uses `__name__` as the package anchor, which makes the two-argument form work as a drop-in replacement for `lazy_loader.attach_stub` in package `__init__.py` files. Passing `None` explicitly preserves `None`. The sibling `.pyi` file is part of the runtime configuration here, not only a type-checking aid.

## 🧩 Supported Stub Forms

The stub parser understands the explicit import forms that the test suite covers:

- `import rich`
- `import rich.console as rich_console`
- `from rich import get_console`
- `from . import cli`
- `from ._factory import make_settings`
- `from ._factory import make_settings as build_settings`

`__all__` stays aligned with the stub definition, and `dir()` includes both declared exports and any names already materialized on the module.

## ⚡ Eager Import Mode

Lazy loading defers import errors until the first attribute access. During development or tests, set `EAGER_IMPORT=1` before importing the package to resolve every declared export immediately.

The current test suite also covers `EAGER_IMPORT=0` for normal lazy behavior and raises a `ValueError` when `EAGER_IMPORT` is set to an invalid boolean string.

## 🚧 Limitations and Errors

- Accessing a name that is not declared in the stub raises `AttributeError`.
- Import failures surface when the lazy attribute is accessed, or earlier if eager mode is enabled.
- The package expects explicit import statements in the sibling stub file and uses that stub file at runtime.

## 🔍 Compared With Alternatives

This project parses the sibling stub AST directly, so the runtime behavior is defined by the same file that type checkers read.

- [`scientific-python/lazy-loader.attach_stub`](https://github.com/scientific-python/lazy-loader) parses stubs into its older `attach(...)` API. In its current implementation, the stub visitor only accepts within-package `from . import ...` and `from .foo import ...` forms and raises `ValueError` for other patterns, so it cannot express absolute entries like `import rich.console as rich_console` in the stub. See the [README](https://github.com/scientific-python/lazy-loader) and [source](https://raw.githubusercontent.com/scientific-python/lazy-loader/main/src/lazy_loader/__init__.py).
- [`etils.epy.lazy_api_imports`](https://etils.readthedocs.io/en/latest/api/epy/lazy_api_imports.html) records imports by temporarily wrapping `builtins.__import__`. Its underlying lazy import helper rejects relative imports with a `ValueError`, so it is not a drop-in fit for sibling package-relative exports. See the [API docs](https://etils.readthedocs.io/en/latest/api/epy/lazy_api_imports.html) and [source](https://cdn.jsdelivr.net/gh/google/etils@main/etils/epy/lazy_api_imports_utils.py).

## ⌨️ Local Development

Clone the repository, install all dependency groups with `uv`, and run the maintained `nox` test matrix:

```bash
gh repo clone liblaf/lazy-loader
cd lazy-loader
mise run install
nox
```

Build the documentation locally with:

```bash
mise run docs:build
```

## 🤝 Contributing

Issues and pull requests are welcome, especially around import edge cases, typing behavior, and documentation improvements.

[![PR Welcome](https://img.shields.io/badge/%F0%9F%A4%AF%20PR%20WELCOME-%E2%86%92-ffcb47?labelColor=black&style=for-the-badge)](https://github.com/liblaf/lazy-loader/pulls)

[![Contributors](https://gh-contributors-gamma.vercel.app/api?repo=liblaf/lazy-loader)](https://github.com/liblaf/lazy-loader/graphs/contributors)

---

#### 📝 License

Copyright © 2026 [liblaf](https://github.com/liblaf). <br />
This project is [MIT](https://github.com/liblaf/lazy-loader/blob/main/LICENSE) licensed.
