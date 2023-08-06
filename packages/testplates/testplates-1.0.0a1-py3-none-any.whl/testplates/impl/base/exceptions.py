__all__ = (
    "TestplatesError",
    "MissingValueError",
    "UnexpectedValueError",
    "ProhibitedValueError",
    "MissingBoundaryError",
    "InvalidSizeError",
    "UnlimitedRangeError",
    "MutuallyExclusiveBoundariesError",
    "OverlappingBoundariesError",
    "SingleMatchBoundariesError",
)

from typing import (
    Any,
)


class TestplatesError(Exception):

    """
    Base testplates error.
    """

    def __init__(
        self,
        message: str,
    ):
        super().__init__(message)

    @property
    def message(self) -> str:

        """
        Returns error message.
        """

        return "".join(self.args)


class MissingValueError(TestplatesError):

    """
    Error indicating missing value.

    Raised when user forgets to set mandatory
    value for given field with actual value.
    """

    def __init__(
        self,
        field: Any,
    ) -> None:
        self.field = field

        super().__init__(f"Missing value for required field {field!r}")


class UnexpectedValueError(TestplatesError):

    """
    Error indicating unexpected value.

    Raised when user passes value which was
    not defined inside the template definition.
    """

    def __init__(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.key = key
        self.value = value

        super().__init__(f"Unexpected key {key!r} with value {value!r}")


class ProhibitedValueError(TestplatesError):

    """
    Error indicating prohibited value.

    Raised when user sets prohibited value that
    is invalid for given field due to its nature.
    """

    def __init__(
        self,
        field: Any,
        value: Any,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(f"Prohibited value {value!r} for field {field!r}")


class MissingBoundaryError(TestplatesError):

    """
    Error indicating missing boundary.

    Raised when user forgets to set mandatory boundary
    for given template with minimum and maximum constraints.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name

        super().__init__(f"Missing value for mandatory boundary {self.name!r}")


class InvalidSizeError(TestplatesError):

    """
    Error indicating invalid size boundary value.

    Raised when user sets size boundary with value
    that does not meet size boundary requirements.
    """

    def __init__(
        self,
        boundary: Any,
    ) -> None:
        self.boundary = boundary

        super().__init__(f"Invalid value for size boundary {boundary!r}")


class UnlimitedRangeError(TestplatesError):

    """
    Error indicating unlimited range.

    Raised when user sets both minimum and maximum
    boundaries to unlimited value in the context that
    does not allow such values to be used there together.
    """

    def __init__(self) -> None:
        super().__init__("Unlimited range is not permitted in this context")


class MutuallyExclusiveBoundariesError(TestplatesError):

    """
    Error indicating exclusive and inclusive boundaries collision.

    Raised when user sets mutually exclusive
    boundaries at the same time with value.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name

        super().__init__(f"Mutually exclusive {name!r} boundaries set at the same time")


class OverlappingBoundariesError(TestplatesError):

    """
    Error indicating overlapping boundaries.

    Raised when user sets both minimum and maximum
    boundaries with values the overlap over each other.
    """

    def __init__(
        self,
        minimum: Any,
        maximum: Any,
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(f"Overlapping minimum {minimum!r} and maximum {maximum!r} boundaries")


class SingleMatchBoundariesError(TestplatesError):

    """
    Error indicating single match boundaries range.

    Raised when user sets boundaries with values that
    creates range which matches only single value.
    """

    def __init__(
        self,
        minimum: Any,
        maximum: Any,
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum

        super().__init__(f"Single match minimum {minimum!r} and maximum {maximum!r} boundaries")
