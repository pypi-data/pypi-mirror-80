__all__ = ("SequenceValidator",)

import typing
import testplates

from typing import (
    Any,
    Union,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_failure,
    Result,
)

from testplates.impl.base import (
    fits_minimum_size,
    fits_maximum_size,
    Limit,
    UnlimitedType,
    TestplatesError,
)

from .utils import (
    has_unique_items,
    Validator,
)

from .type import (
    TypeValidator,
)

from .exceptions import (
    ItemValidationError,
    InvalidMinimumSizeError,
    InvalidMaximumSizeError,
    UniquenessError,
)

Boundary = Union[UnlimitedType, Limit]

sequence_type_validator: Final[Validator] = TypeValidator(typing.Sequence)


class SequenceValidator:

    __slots__ = (
        "item_validator",
        "minimum_size",
        "maximum_size",
        "unique_items",
    )

    def __init__(
        self,
        item_validator: Validator,
        /,
        *,
        minimum_size: Boundary,
        maximum_size: Boundary,
        unique_items: bool,
    ) -> None:
        self.item_validator = item_validator
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size
        self.unique_items = unique_items

    def __repr__(self) -> str:
        return f"{testplates.__name__}.sequence_validator()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := sequence_type_validator(data)):
            return failure(result)

        item_validator = self.item_validator

        for item in data:
            if not (result := item_validator(item)):
                return failure(ItemValidationError(data, item, unwrap_failure(result)))

        if not fits_minimum_size(data, self.minimum_size):
            return failure(InvalidMinimumSizeError(data, self.minimum_size))

        if not fits_maximum_size(data, self.maximum_size):
            return failure(InvalidMaximumSizeError(data, self.maximum_size))

        if self.unique_items and not has_unique_items(data):
            return failure(UniquenessError(data))

        return success(None)
