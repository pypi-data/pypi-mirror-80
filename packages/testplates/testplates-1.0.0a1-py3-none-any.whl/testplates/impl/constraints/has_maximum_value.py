__all__ = ("HasMaximumValue",)

import testplates

from typing import (
    Any,
    Union,
)

from testplates.impl.base import (
    fits_maximum_value,
    Limit,
    UnlimitedType,
)

Boundary = Union[Limit, UnlimitedType]


class HasMaximumValue:

    __slots__ = (
        "name",
        "maximum_value",
    )

    def __init__(
        self,
        name: str,
        maximum_value: Boundary,
        /,
    ) -> None:
        self.name = name
        self.maximum_value = maximum_value

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.maximum_value!r})"

    def __eq__(self, other: Any) -> bool:
        return fits_maximum_value(other, self.maximum_value)
