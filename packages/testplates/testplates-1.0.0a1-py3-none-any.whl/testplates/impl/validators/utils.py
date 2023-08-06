__all__ = (
    "is_classinfo",
    "has_unique_items",
    "Validator",
)

from typing import (
    Any,
    Iterable,
    Hashable,
    Callable,
)

from resultful import (
    Result,
)

from testplates.impl.base import (
    TestplatesError,
)

Validator = Callable[[Any], Result[None, TestplatesError]]


def is_classinfo(
    classinfo: type,
    /,
) -> bool:
    try:
        isinstance(object, classinfo)
    except TypeError:
        return False
    else:
        return True


def has_unique_items(
    items: Iterable[Hashable],
) -> bool:
    visited = set()

    for item in items:
        if item in visited:
            return False
        else:
            visited.add(item)

    return True
