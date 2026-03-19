import sys

import pytest


@pytest.fixture(autouse=True)
def clean_fake_pkg(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("EAGER_IMPORT", raising=False)
    if (tests_module := sys.modules.get("tests")) is not None and hasattr(
        tests_module, "fake_pkg"
    ):
        delattr(tests_module, "fake_pkg")
    sys.modules.pop("rich", None)
    sys.modules.pop("rich.abc", None)
    sys.modules.pop("rich.console", None)
    sys.modules.pop("tests.fake_pkg", None)
    sys.modules.pop("tests.fake_pkg._from_import_as", None)
    sys.modules.pop("tests.fake_pkg._from_import", None)
    sys.modules.pop("tests.fake_pkg._import_as", None)
    sys.modules.pop("tests.fake_pkg._import", None)
    sys.modules.pop("tests.fake_pkg.e", None)
