__all__ = ("HasSize",)

import testplates

from typing import (
    Any,
    Sized,
)


class HasSize:

    __slots__ = (
        "name",
        "size",
    )

    def __init__(
        self,
        name: str,
        size: int,
        /,
    ) -> None:
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.size})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Sized):
            return False

        return len(other) == self.size
