import pytest


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
    assert dir(fake_pkg) == expected
    assert fake_pkg.__all__ == expected


def test_attribute_error() -> None:
    from . import fake_pkg

    with pytest.raises(
        AttributeError, match=r"module 'tests.fake_pkg' has no attribute 'non_exist'"
    ):
        fake_pkg.non_exist  # noqa: B018  # ty:ignore[unresolved-attribute]


def test_import_error() -> None:
    with pytest.raises(
        ImportError, match=r"cannot import name 'non_exist' from 'tests.fake_pkg'"
    ):
        from .fake_pkg import non_exist  # noqa: F401  # ty:ignore[unresolved-import]
