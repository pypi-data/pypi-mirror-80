__all__ = ("HasMinimumValue",)

import testplates

from typing import (
    Any,
    Union,
)

from testplates.impl.base import (
    fits_minimum_value,
    Limit,
    UnlimitedType,
)

Boundary = Union[Limit, UnlimitedType]


class HasMinimumValue:

    __slots__ = (
        "name",
        "minimum_value",
    )

    def __init__(
        self,
        name: str,
        minimum_value: Boundary,
        /,
    ) -> None:
        self.name = name
        self.minimum_value = minimum_value

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.minimum_value!r})"

    def __eq__(self, other: Any) -> bool:
        return fits_minimum_value(other, self.minimum_value)
