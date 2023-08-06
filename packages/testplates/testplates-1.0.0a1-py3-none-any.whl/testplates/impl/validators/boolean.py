__all__ = ("BooleanValidator",)

import testplates

from typing import (
    Any,
    Final,
)

from resultful import (
    Result,
)

from testplates.impl.base import (
    TestplatesError,
)

from .utils import (
    Validator,
)

from .type import (
    TypeValidator,
)

boolean_type_validator: Final[Validator] = TypeValidator(bool)


class BooleanValidator:

    __slots__ = ()

    def __repr__(self) -> str:
        return f"{testplates.__name__}.boolean_validator()"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        return boolean_type_validator(data)
