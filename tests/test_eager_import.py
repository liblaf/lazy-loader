import importlib
import inspect
import sys

import pytest


def test_eager_import_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EAGER_IMPORT", "1")

    assert "tests.fake_pkg" not in sys.modules
    assert "tests.fake_pkg._from_import" not in sys.modules
    assert "tests.fake_pkg._from_import_as" not in sys.modules
    assert "tests.fake_pkg._import" not in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules
    assert "rich" not in sys.modules
    assert "rich.console" not in sys.modules

    from tests import fake_pkg

    assert "tests.fake_pkg._from_import" in sys.modules
    assert "tests.fake_pkg._from_import_as" in sys.modules
    assert "tests.fake_pkg._import" in sys.modules
    assert "tests.fake_pkg._import_as" in sys.modules
    assert "tests.fake_pkg.e" in sys.modules
    assert "rich" in sys.modules
    assert "rich.console" in sys.modules
    assert fake_pkg.a == 1
    assert fake_pkg.b == 2
    assert fake_pkg.c == 3
    assert fake_pkg.d == 4
    assert inspect.ismodule(fake_pkg.e)
    assert inspect.ismodule(fake_pkg.rich)
    assert inspect.ismodule(fake_pkg.console)
    assert fake_pkg.get_console is fake_pkg.rich.get_console
    assert fake_pkg.rich_console is sys.modules["rich.console"]


def test_eager_import_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EAGER_IMPORT", "0")

    assert "tests.fake_pkg" not in sys.modules
    assert "tests.fake_pkg._from_import" not in sys.modules
    assert "tests.fake_pkg._from_import_as" not in sys.modules
    assert "tests.fake_pkg._import" not in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules
    assert "rich" not in sys.modules
    assert "rich.console" not in sys.modules

    from tests import fake_pkg

    assert "tests.fake_pkg._from_import" not in sys.modules
    assert "tests.fake_pkg._from_import_as" not in sys.modules
    assert "tests.fake_pkg._import" not in sys.modules
    assert "tests.fake_pkg._import_as" not in sys.modules
    assert "tests.fake_pkg.e" not in sys.modules
    assert "rich" not in sys.modules
    assert "rich.console" not in sys.modules
    assert fake_pkg.a == 1
    assert fake_pkg.b == 2
    assert fake_pkg.c == 3
    assert fake_pkg.d == 4
    assert inspect.ismodule(fake_pkg.e)
    assert inspect.ismodule(fake_pkg.rich)
    assert inspect.ismodule(fake_pkg.console)
    assert fake_pkg.get_console is fake_pkg.rich.get_console
    assert fake_pkg.rich_console is sys.modules["rich.console"]


def test_eager_import_invalid_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EAGER_IMPORT", "invalid")
    with pytest.raises(ValueError, match="EAGER_IMPORT"):
        importlib.import_module("tests.fake_pkg")
