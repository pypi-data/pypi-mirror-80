from __future__ import annotations

__all__ = (
    "is_value",
    "values_matches",
    "MissingType",
    "SpecialValueType",
    "UnlimitedType",
    "SecretType",
    "Maybe",
    "Value",
    "Validator",
    "ANY",
    "WILDCARD",
    "ABSENT",
    "MISSING",
    "UNLIMITED",
)

import enum
import testplates

from typing import (
    Any,
    TypeVar,
    Union,
    Callable,
    Literal,
    Final,
)

from resultful import (
    Result,
)

from .exceptions import (
    TestplatesError,
)


# noinspection PyUnresolvedReferences
def is_value(
    value: Maybe[Value[Any]],
) -> bool:

    """
    Returns True if value is not missing
    or a special value, otherwise False.

    :param value: template value
    """

    return value not in [MISSING, ANY, ABSENT, WILDCARD]


# noinspection PyUnresolvedReferences
def values_matches(
    self_value: Maybe[Value[_GenericType]],
    other_value: Maybe[Value[_GenericType]],
    /,
) -> bool:

    """
    Compares self value and other value and
    returns True if they match, otherwise False.

    Assumes that special values were validated
    against field types and do not bend any logic.

    :param self_value: self template value
    :param other_value: other object value
    """

    if self_value is WILDCARD:
        return True

    if self_value is ANY and other_value is not MISSING:
        return True

    if self_value is ABSENT and other_value is MISSING:
        return True

    return self_value == other_value


# noinspection PyFinal
class MissingType(enum.Enum):

    """
    Missing value type class.
    """

    MISSING = enum.auto()

    """
        Indicator for missing value.
    """

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}"


# noinspection PyFinal
class SpecialValueType(enum.Enum):

    """
    Special value type class.
    """

    ANY = enum.auto()

    """
        Works for both required and optional fields.
        Matches the corresponding field if, and only if, the field value is present.
    """

    WILDCARD = enum.auto()

    """
        Works for optional fields only.
        Matches the corresponding field if either the field value is present or absent.
    """

    ABSENT = enum.auto()

    """
        Works for optional fields only.
        Matches the corresponding field if, and only if, the field value is absent.
    """

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}"


# noinspection PyFinal
class UnlimitedType(enum.Enum):

    """
    Unlimited value type class.
    """

    UNLIMITED = enum.auto()

    """
        Indicator for unlimited value.
    """

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}"


class SecretType(enum.Enum):

    """
    Secret value type class.

    FOR INTERNAL USE ONLY.
    """

    SECRET = enum.auto()

    """
        Secret internal value.
    """


_GenericType = TypeVar("_GenericType")

Maybe = Union[_GenericType, MissingType]
Value = Union[_GenericType, SpecialValueType]
Validator = Callable[[Any], Result[None, TestplatesError]]

ANY: Final[Literal[SpecialValueType.ANY]] = SpecialValueType.ANY
WILDCARD: Final[Literal[SpecialValueType.WILDCARD]] = SpecialValueType.WILDCARD
ABSENT: Final[Literal[SpecialValueType.ABSENT]] = SpecialValueType.ABSENT
MISSING: Final[Literal[MissingType.MISSING]] = MissingType.MISSING
UNLIMITED: Final[Literal[UnlimitedType.UNLIMITED]] = UnlimitedType.UNLIMITED
