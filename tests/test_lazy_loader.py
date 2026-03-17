import inspect
import sys

import pytest


@pytest.fixture
def clean_fake_pkg() -> None:
    sys.modules.pop("rich", None)
    sys.modules.pop("tests.fake_pkg", None)
    sys.modules.pop("tests.fake_pkg._from_import_as", None)
    sys.modules.pop("tests.fake_pkg._from_import", None)
    sys.modules.pop("tests.fake_pkg._import_as", None)
    sys.modules.pop("tests.fake_pkg._import", None)
    sys.modules.pop("tests.fake_pkg.e", None)


def test_relative(clean_fake_pkg: None) -> None:  # noqa: ARG001
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


def test_absolute(clean_fake_pkg: None) -> None:  # noqa: ARG001
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
