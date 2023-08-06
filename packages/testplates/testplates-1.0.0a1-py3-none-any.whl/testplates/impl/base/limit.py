from __future__ import annotations

__all__ = (
    "Limit",
    "Extremum",
    "MINIMUM_EXTREMUM",
    "MAXIMUM_EXTREMUM",
)

from typing import (
    Literal,
    Final,
)

Extremum = Literal["minimum", "maximum"]

MINIMUM_EXTREMUM: Final[Literal["minimum"]] = "minimum"
MAXIMUM_EXTREMUM: Final[Literal["maximum"]] = "maximum"

INCLUSIVE_ALIGNMENT: Final[Literal[0]] = 0
EXCLUSIVE_ALIGNMENT: Final[Literal[1]] = 1


class Limit:

    __slots__ = (
        "name",
        "value",
        "is_inclusive",
    )

    def __init__(
        self,
        name: Extremum,
        value: int,
        /,
        *,
        is_inclusive: bool,
    ) -> None:
        self.name = name
        self.value = value
        self.is_inclusive = is_inclusive

    def __repr__(self) -> str:
        prefix = "" if self.is_inclusive else "exclusive_"

        return f"{prefix}{self.name}={self.value}"

    @property
    def alignment(self) -> Literal[0, 1]:

        """
        Returns limit alignment.

        Alignment indicates whether we accept the value
        equal to the limit value as correct one or not.

        If alignment is equal to 0, value equal to limit is accepted.
        If alignment is equal to 1, value equal to limit is not accepted.
        """

        return INCLUSIVE_ALIGNMENT if self.is_inclusive else EXCLUSIVE_ALIGNMENT
