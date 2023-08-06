__all__ = ("HasSizeBetween",)

import testplates

from typing import (
    Any,
    Union,
    Sized,
)

from testplates.impl.base import (
    fits_minimum_size,
    fits_maximum_size,
    Limit,
    UnlimitedType,
)

Boundary = Union[Limit, UnlimitedType]


class HasSizeBetween:

    __slots__ = (
        "name",
        "minimum_size",
        "maximum_size",
    )

    def __init__(
        self,
        name: str,
        /,
        *,
        minimum_size: Boundary,
        maximum_size: Boundary,
    ) -> None:
        self.name = name
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size

    def __repr__(self) -> str:
        boundaries = [
            repr(self.minimum_size),
            repr(self.maximum_size),
        ]

        return f"{testplates.__name__}.{self.name}({', '.join(boundaries)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        minimum_fits = fits_minimum_size(other, self.minimum_size)
        maximum_fits = fits_maximum_size(other, self.maximum_size)

        return minimum_fits and maximum_fits
