__all__ = ("HasMinimumSize",)

import testplates

from typing import (
    Any,
    Union,
    Sized,
)

from testplates.impl.base import (
    fits_minimum_size,
    Limit,
    UnlimitedType,
)

Boundary = Union[Limit, UnlimitedType]


class HasMinimumSize:

    __slots__ = (
        "name",
        "minimum_size",
    )

    def __init__(
        self,
        name: str,
        minimum_size: Boundary,
        /,
    ) -> None:
        self.name = name
        self.minimum_size = minimum_size

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.minimum_size!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return fits_minimum_size(other, self.minimum_size)
