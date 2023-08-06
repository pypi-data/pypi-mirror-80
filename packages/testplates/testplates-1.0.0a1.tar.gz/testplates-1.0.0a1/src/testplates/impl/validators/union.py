__all__ = ("UnionValidator",)

import testplates

from typing import (
    Any,
    Mapping,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_failure,
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

from .exceptions import (
    InvalidKeyError,
    InvalidDataFormatError,
    ChoiceValidationError,
)

union_type_validator: Final[Validator] = TypeValidator(tuple)


class UnionValidator:

    __slots__ = ("choices",)

    def __init__(
        self,
        choices: Mapping[str, Validator],
        /,
    ) -> None:
        self.choices = choices

    def __repr__(self) -> str:
        return f"{testplates.__name__}.union_validator({self.choices})"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        if not (result := union_type_validator(data)):
            return failure(result)

        try:
            key, value = data
        except ValueError:
            return failure(InvalidDataFormatError(data))

        choice_validator = self.choices.get(key, None)

        if choice_validator is None:
            return failure(InvalidKeyError(key, data))

        if not (result := choice_validator(value)):
            return failure(ChoiceValidationError(data, choice_validator, unwrap_failure(result)))

        return success(None)
