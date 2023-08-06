__all__ = ("get_pattern",)

import re

from typing import (
    AnyStr,
    Pattern,
    Optional,
)


def get_pattern(
    pattern: Optional[AnyStr],
) -> Optional[Pattern[AnyStr]]:

    """
    Returns compiled pattern if string pattern is not None, otherwise None.
    """

    return re.compile(pattern) if pattern is not None else None
