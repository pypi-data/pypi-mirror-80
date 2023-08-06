__all__ = (
    "Maybe",
    "Value",
    "Boundary",
    "Validator",
    "LiteralMissing",
    "LiteralAny",
    "LiteralWildcard",
    "LiteralAbsent",
    "LiteralUnlimited",
    "MISSING",
    "ANY",
    "WILDCARD",
    "ABSENT",
    "UNLIMITED",
)

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

from testplates.impl.base import (
    MissingType,
    SpecialValueType,
    UnlimitedType,
)

from .exceptions import (
    TestplatesError,
)

_GenericType = TypeVar("_GenericType")

Maybe = Union[_GenericType, MissingType]
Value = Union[_GenericType, SpecialValueType]
Boundary = Union[_GenericType, UnlimitedType]
Validator = Callable[[Any], Result[None, TestplatesError]]

LiteralMissing = Literal[MissingType.MISSING]
LiteralAny = Literal[SpecialValueType.ANY]
LiteralWildcard = Literal[SpecialValueType.WILDCARD]
LiteralAbsent = Literal[SpecialValueType.ABSENT]
LiteralUnlimited = Literal[UnlimitedType.UNLIMITED]

MISSING: Final[LiteralMissing] = MissingType.MISSING
ANY: Final[LiteralAny] = SpecialValueType.ANY
WILDCARD: Final[LiteralWildcard] = SpecialValueType.WILDCARD
ABSENT: Final[LiteralAbsent] = SpecialValueType.ABSENT
UNLIMITED: Final[LiteralUnlimited] = UnlimitedType.UNLIMITED
