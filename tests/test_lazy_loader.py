import inspect
import sys
from typing import cast

from liblaf.lazy_loader import LazyLoader, attach_stub


def test_dir() -> None:
    from . import fake_pkg

    expected: list[str] = [
        "a",
        "b",
        "c",
        "console",
        "d",
        "e",
        "get_console",
        "rich",
        "rich_console",
    ]
    assert fake_pkg.__all__ == expected
    assert set(dir(fake_pkg)) >= set(expected)


def test_relative() -> None:
    assert "tests.fake_pkg" not in sys.modules
    assert "tests.fake_pkg._from_import" not in sys.modules
    assert "tests.fake_pkg._from_import_as" not in sys.modules
    assert "tests.fake_pkg._import" not in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules

    from . import fake_pkg

    assert fake_pkg.a == 1
    assert "tests.fake_pkg._from_import" in sys.modules
    assert "tests.fake_pkg._from_import_as" not in sys.modules
    assert "tests.fake_pkg._import" not in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules

    assert fake_pkg.b == 2
    assert "tests.fake_pkg._from_import" in sys.modules
    assert "tests.fake_pkg._from_import_as" in sys.modules
    assert "tests.fake_pkg._import" not in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules

    assert fake_pkg.c == 3
    assert "tests.fake_pkg._from_import" in sys.modules
    assert "tests.fake_pkg._from_import_as" in sys.modules
    assert "tests.fake_pkg._import" in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules

    assert fake_pkg.d == 4
    assert "tests.fake_pkg._from_import" in sys.modules
    assert "tests.fake_pkg._from_import_as" in sys.modules
    assert "tests.fake_pkg._import" in sys.modules
    assert "tests.fake_pkg._import_as" in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules

    assert inspect.ismodule(fake_pkg.e)
    assert "tests.fake_pkg._from_import" in sys.modules
    assert "tests.fake_pkg._from_import_as" in sys.modules
    assert "tests.fake_pkg._import" in sys.modules
    assert "tests.fake_pkg._import_as" in sys.modules
    assert "tests.fake_pkg.e" in sys.modules


def test_absolute() -> None:
    assert "rich" not in sys.modules

    from . import fake_pkg

    assert inspect.ismodule(fake_pkg.rich)
    assert "rich" in sys.modules

    import rich
    import rich.console as rich_console

    assert fake_pkg.console is rich_console
    assert fake_pkg.get_console is rich.get_console
    assert fake_pkg.rich is rich
    assert fake_pkg.rich_console is rich_console


def test_attach_stub_accepts_package_as_last_arg() -> None:
    from . import fake_pkg

    getattr_, dir_, exports = attach_stub(
        fake_pkg.__name__, fake_pkg.__file__, fake_pkg.__package__
    )
    loader: LazyLoader = cast("LazyLoader", getattr_.__self__)  # ty:ignore[unresolved-attribute]

    assert loader.package == fake_pkg.__package__
    assert exports == fake_pkg.__all__
    assert set(dir_()) >= set(exports)
    assert getattr_("a") == 1
