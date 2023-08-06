__all__ = ("MatchesPattern",)

import re
import abc
import testplates

from typing import (
    Any,
    AnyStr,
    Type,
    Generic,
    Pattern,
)


class MatchesPattern(Generic[AnyStr], abc.ABC):

    __slots__ = (
        "name",
        "pattern",
        "pattern_type",
    )

    def __init__(
        self,
        name: str,
        value: AnyStr,
        /,
    ) -> None:
        self.name = name
        self.pattern: Pattern[AnyStr] = re.compile(value)
        self.pattern_type: Type[AnyStr] = type(value)

    def __repr__(self) -> str:
        return f"{testplates.__name__}.{self.name}({self.pattern.pattern!r})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.pattern_type):
            return False

        return bool(self.pattern.match(other))
