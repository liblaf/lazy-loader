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

`liblaf-lazy-loader` lets Python packages expose imports lazily from a sibling stub file, so modules stay lightweight until an attribute is actually used.

## ✨ Features

- 💤 **Stub-driven lazy imports:** Parse a sibling `.pyi` file and turn its `import` and `from ... import ...` statements into on-demand attribute loaders.
- 📦 **Module-friendly exports:** Preserve `__all__` and enrich `dir()` so interactive use and star exports stay aligned with the stub definition.
- 🔁 **Absolute and relative import support:** Handle both local package imports and external modules, including aliased imports.
- ⚡ **Optional eager mode:** Set `EAGER_IMPORT=1` to resolve every declared export at import time when startup indirection is not wanted.
- 🧭 **Typed, tiny surface area:** Ship as a typed package with no runtime dependencies and a small public API centered on `attach_stub` and `LazyLoader`.

## 📦 Installation

> [!NOTE]
> `liblaf-lazy-loader` requires Python 3.12 or newer.

```bash
uv add liblaf-lazy-loader
```

## 🚀 Quick Start

Expose lazy attributes from your package `__init__.py`:

```python
from liblaf.lazy_loader import attach_stub

__getattr__, __dir__, __all__ = attach_stub(__name__, __package__, __file__)
```

Define the exported imports in the sibling `__init__.pyi`:

```python
from ._core import Widget
from ._helpers import make_widget
import rich.console as rich_console

__all__ = ["Widget", "make_widget", "rich_console"]
```

With that wiring in place, `Widget`, `make_widget`, and `rich_console` are imported only when first accessed. If you need everything loaded immediately, set `EAGER_IMPORT=1` before importing the package.

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
