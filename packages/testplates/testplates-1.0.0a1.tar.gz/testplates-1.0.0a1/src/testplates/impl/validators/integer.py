__all__ = ("IntegerValidator",)

import testplates

from typing import (
    Any,
    Union,
    Final,
)

from resultful import (
    success,
    failure,
    Result,
)

from testplates.impl.base import (
    fits_minimum_value,
    fits_maximum_value,
    Limit,
    UnlimitedType,
    TestplatesError,
)

from .type import (
    TypeValidator,
)

from .exceptions import (
    InvalidMinimumValueError,
    InvalidMaximumValueError,
    ProhibitedBoolValueError,
)

Boundary = Union[Limit, UnlimitedType]

validate_integer_type: Final = TypeValidator(int)


class IntegerValidator:

    __slots__ = (
        "minimum_value",
        "maximum_value",
        "allow_bool",
    )

    def __init__(
        self,
        *,
        minimum_value: Boundary,
        maximum_value: Boundary,
        allow_bool: bool,
    ) -> None:
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.allow_bool = allow_bool

    def __repr__(self) -> str:
        return f"{testplates.__name__}.integer_validator()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := validate_integer_type(data)):
            return failure(result)

        if not (result := validate_bool_type(data, self.allow_bool)):
            return failure(result)

        if not (result := validate_boundaries(data, self.minimum_value, self.maximum_value)):
            return failure(result)

        return success(None)


def validate_bool_type(
    data: int,
    allow_bool: bool,
    /,
) -> Result[None, TestplatesError]:
    if not allow_bool and isinstance(data, bool):
        return failure(ProhibitedBoolValueError(data))

    return success(None)


def validate_boundaries(
    data: int,
    minimum_value: Boundary,
    maximum_value: Boundary,
    /,
) -> Result[None, TestplatesError]:
    if not fits_minimum_value(data, minimum_value):
        return failure(InvalidMinimumValueError(data, minimum_value))

    if not fits_maximum_value(data, maximum_value):
        return failure(InvalidMaximumValueError(data, maximum_value))

    return success(None)
