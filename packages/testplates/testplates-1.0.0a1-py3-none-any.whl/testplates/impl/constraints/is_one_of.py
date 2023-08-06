__all__ = ("IsOneOf",)

import testplates

from typing import (
    Any,
    TypeVar,
    Generic,
)

from testplates.impl.utils import (
    format_like_tuple,
)

_GenericType = TypeVar("_GenericType")


class IsOneOf(Generic[_GenericType]):

    __slots__ = (
        "name",
        "values",
    )

    def __init__(
        self,
        name: str,
        /,
        *values: _GenericType,
    ) -> None:
        self.name = name
        self.values = values

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({format_like_tuple(self.values)})"

    def __eq__(self, other: Any) -> bool:
        return other in self.values
