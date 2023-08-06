__all__ = (
    "StringValidator",
    "BytesValidator",
)

import testplates

from typing import (
    Any,
    AnyStr,
    Union,
    Pattern,
    Optional,
    Final,
)

from resultful import (
    success,
    failure,
    Result,
)

from testplates.impl.base import (
    fits_minimum_size,
    fits_maximum_size,
    Limit,
    UnlimitedType,
    TestplatesError,
)

from .type import (
    TypeValidator,
)

from .exceptions import (
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    InvalidFormatError,
)

Boundary = Union[Limit, UnlimitedType]

string_type_validator: Final = TypeValidator(str)
bytes_type_validator: Final = TypeValidator(bytes)


class StringValidator:

    __slots__ = (
        "minimum_size",
        "maximum_size",
        "pattern",
    )

    def __init__(
        self,
        *,
        minimum_size: Boundary,
        maximum_size: Boundary,
        pattern: Optional[Pattern[str]],
    ) -> None:
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size
        self.pattern = pattern

    def __repr__(self) -> str:
        return f"{testplates.__name__}.string_validator()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := string_type_validator(data)):
            return failure(result)

        if not (result := validate_size(data, self.minimum_size, self.maximum_size)):
            return failure(result)

        if not (result := validate_pattern(data, self.pattern)):
            return failure(result)

        return success(None)


class BytesValidator:

    __slots__ = (
        "minimum_size",
        "maximum_size",
        "pattern",
    )

    def __init__(
        self,
        *,
        minimum_size: Boundary,
        maximum_size: Boundary,
        pattern: Optional[Pattern[bytes]],
    ) -> None:
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size
        self.pattern = pattern

    def __repr__(self) -> str:
        return f"{testplates.__name__}.bytes_validator()"

    def __call__(self, data: Any) -> Result[None, TestplatesError]:
        if not (result := bytes_type_validator(data)):
            return failure(result)

        if not (result := validate_size(data, self.minimum_size, self.maximum_size)):
            return failure(result)

        if not (result := validate_pattern(data, self.pattern)):
            return failure(result)

        return success(None)


def validate_size(
    data: AnyStr,
    minimum_size: Boundary,
    maximum_size: Boundary,
    /,
) -> Result[None, TestplatesError]:
    if not fits_minimum_size(data, minimum_size):
        return failure(InvalidMinimumSizeError(data, minimum_size))

    if not fits_maximum_size(data, maximum_size):
        return failure(InvalidMaximumSizeError(data, maximum_size))

    return success(None)


def validate_pattern(
    data: AnyStr,
    pattern: Optional[Pattern[AnyStr]],
    /,
) -> Result[None, TestplatesError]:
    if pattern is not None:
        if not pattern.match(data):
            return failure(InvalidFormatError(data, pattern))

    return success(None)
