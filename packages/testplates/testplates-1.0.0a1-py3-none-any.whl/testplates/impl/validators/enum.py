__all__ = ("EnumValidator",)

import testplates

from enum import (
    EnumMeta,
)

from typing import (
    Any,
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


class EnumValidator:

    __slots__ = (
        "enum_type",
        "enum_type_validator",
        "enum_member_validator",
    )

    def __init__(
        self,
        enum_type: EnumMeta,
        *,
        enum_type_validator: Validator,
        enum_member_validator: Validator,
    ) -> None:
        self.enum_type = enum_type
        self.enum_type_validator = enum_type_validator
        self.enum_member_validator = enum_member_validator

    def __repr__(self) -> str:
        parameters = f"{self.enum_type}, {self.enum_member_validator}"

        return f"{testplates.__name__}.enum_validator({parameters})"

    def __call__(self, data: Any, /) -> Result[None, TestplatesError]:
        return self.enum_type_validator(data)
