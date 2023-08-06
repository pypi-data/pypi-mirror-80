__all__ = ("HasValueBetween",)

import testplates

from typing import (
    Any,
    Union,
)

from testplates.impl.base import (
    fits_minimum_value,
    fits_maximum_value,
    Limit,
    UnlimitedType,
)

Boundary = Union[Limit, UnlimitedType]


class HasValueBetween:

    __slots__ = (
        "name",
        "minimum_value",
        "maximum_value",
    )

    def __init__(
        self,
        name: str,
        /,
        *,
        minimum_value: Boundary,
        maximum_value: Boundary,
    ) -> None:
        self.name = name
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value

    def __repr__(self) -> str:
        boundaries = [
            repr(self.minimum_value),
            repr(self.maximum_value),
        ]

        return f"{testplates.__name__}.{self.name}({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        minimum_fits = fits_minimum_value(other, self.minimum_value)
        maximum_fits = fits_maximum_value(other, self.maximum_value)

        return minimum_fits and maximum_fits
