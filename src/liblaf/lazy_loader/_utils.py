import enum
import os


class MissingType(enum.Enum):
    MISSING = enum.auto()


MISSING: MissingType = MissingType.MISSING


# ref: <https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Bool>
_ENV_BOOL_FALSY: set[str] = {
    "0",
    "F",
    "FALSE",
    "False",
    "N",
    "NO",
    "No",
    "OFF",
    "Off",
    "f",
    "false",
    "n",
    "no",
    "off",
}
_ENV_BOOL_TRUTHY: set[str] = {
    "1",
    "ON",
    "On",
    "T",
    "TRUE",
    "True",
    "Y",
    "YES",
    "Yes",
    "on",
    "t",
    "true",
    "y",
    "yes",
}


def env_bool(name: str, default: bool = False) -> bool:  # noqa: FBT001, FBT002
    value: str | None = os.getenv(name)
    if value is None:
        return default
    if value in _ENV_BOOL_TRUTHY:
        return True
    if value in _ENV_BOOL_FALSY:
        return False
    msg: str = f"Environment variable {name!r} invalid: Not a valid boolean."
    raise ValueError(msg)
