__all__ = ("HasMaximumSize",)

import testplates

from typing import (
    Any,
    Union,
    Sized,
)

from testplates.impl.base import (
    fits_maximum_size,
    Limit,
    UnlimitedType,
)

Boundary = Union[Limit, UnlimitedType]


class HasMaximumSize:

    __slots__ = (
        "name",
        "maximum_size",
    )

    def __init__(
        self,
        name: str,
        maximum_size: Boundary,
        /,
    ) -> None:
        self.name = name
        self.maximum_size = maximum_size

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.maximum_size!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return fits_maximum_size(other, self.maximum_size)
