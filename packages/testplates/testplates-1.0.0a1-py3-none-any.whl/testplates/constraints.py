__all__ = (
    "contains",
    "has_size",
    "has_minimum_size",
    "has_maximum_size",
    "has_size_between",
    "has_minimum_value",
    "has_maximum_value",
    "has_value_between",
    "is_one_of",
    "is_permutation_of",
    "matches_pattern",
)

from typing import (
    overload,
    AnyStr,
    TypeVar,
    List,
    Optional,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    Result,
    AlwaysFailure,
)

from testplates.impl.base import (
    get_minimum_value,
    get_maximum_value,
    get_minimum_size,
    get_maximum_size,
    get_value_boundaries,
    get_size_boundaries,
)

from testplates.impl.constraints import (
    Contains,
    HasSize,
    HasMinimumSize,
    HasMaximumSize,
    HasSizeBetween,
    HasMinimumValue,
    HasMaximumValue,
    HasValueBetween,
    IsOneOf,
    IsPermutationOf,
    MatchesPattern,
)

from .value import (
    Boundary,
    UNLIMITED,
)

from .exceptions import (
    TestplatesError,
    UnlimitedRangeError,
)

_GenericType = TypeVar("_GenericType")


def contains(
    first: _GenericType,
    /,
    *rest: _GenericType,
) -> Result[Contains[_GenericType], TestplatesError]:

    """
    Returns constraint object that matches any container object
    that contains all values specified via the positional arguments.

    :param first: first value to be present in the container object
    :param rest: other values to be present in container object
    """

    return success(Contains(contains.__name__, first, *rest))


def has_size(
    size: int,
) -> Result[HasSize, TestplatesError]:

    """
    Returns constraint object that matches any sized
    object that has size equal to the exact value.

    :param size: exact size
    """

    return success(HasSize(has_size.__name__, size))


def has_minimum_size(
    minimum: int,
    /,
) -> Result[HasMinimumSize, TestplatesError]:

    """
    Returns constraint object that matches any sized
    object that has size above minimum boundary value.

    :param minimum: minimum size
    """

    result = get_minimum_size(minimum)

    if not result:
        return result

    minimum_size_boundary = unwrap_success(result)

    return success(HasMinimumSize(has_minimum_size.__name__, minimum_size_boundary))


def has_maximum_size(
    maximum: int,
    /,
) -> Result[HasMaximumSize, TestplatesError]:

    """
    Returns constraint object that matches any sized
    object that has size below maximum boundary value.

    :param maximum: maximum size
    """

    result = get_maximum_size(maximum)

    if not result:
        return result

    maximum_size_boundary = unwrap_success(result)

    return success(HasMaximumSize(has_maximum_size.__name__, maximum_size_boundary))


def has_size_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
) -> Result[HasSizeBetween, TestplatesError]:

    """
    Returns constraint object that matches any sized object
    that has size between minimum and maximum boundaries values.

    :param minimum: minimum size boundary value
    :param maximum: maximum size boundary value
    """

    if minimum is UNLIMITED and maximum is UNLIMITED:
        return failure(UnlimitedRangeError())

    result = get_size_boundaries(inclusive_minimum=minimum, inclusive_maximum=maximum)

    if not result:
        return result

    minimum_size_boundary, maximum_size_boundary = unwrap_success(result)

    return success(
        HasSizeBetween(
            has_size_between.__name__,
            minimum_size=minimum_size_boundary,
            maximum_size=maximum_size_boundary,
        )
    )


@overload
def has_minimum_value() -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_minimum_value(
    *,
    minimum: int,
    exclusive_minimum: int,
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_minimum_value(
    *,
    minimum: int,
) -> Result[HasMinimumValue, TestplatesError]:
    ...


@overload
def has_minimum_value(
    *,
    exclusive_minimum: int,
) -> Result[HasMinimumValue, TestplatesError]:
    ...


def has_minimum_value(
    *,
    minimum: Optional[int] = None,
    exclusive_minimum: Optional[int] = None,
) -> Result[HasMinimumValue, TestplatesError]:

    """
    Returns constraint object that matches any object
    with boundaries support above minimum boundary value.

    :param minimum: minimum value
    :param exclusive_minimum: exclusive minimum value
    """

    result = get_minimum_value(inclusive=minimum, exclusive=exclusive_minimum)

    if not result:
        return result

    minimum_value_boundary = unwrap_success(result)

    return success(HasMinimumValue(has_minimum_value.__name__, minimum_value_boundary))


@overload
def has_maximum_value() -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_maximum_value(
    *,
    maximum: int,
    exclusive_maximum: int,
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_maximum_value(
    *,
    maximum: int,
) -> Result[HasMaximumValue, TestplatesError]:
    ...


@overload
def has_maximum_value(
    *,
    exclusive_maximum: int,
) -> Result[HasMaximumValue, TestplatesError]:
    ...


def has_maximum_value(
    *,
    maximum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
) -> Result[HasMaximumValue, TestplatesError]:

    """
    Returns constraint object that matches any object
    with boundaries support below maximum boundary value.

    :param maximum: maximum value
    :param exclusive_maximum: exclusive maximum value
    """

    result = get_maximum_value(inclusive=maximum, exclusive=exclusive_maximum)

    if not result:
        return result

    maximum_value_boundary = unwrap_success(result)

    return success(HasMaximumValue(has_maximum_value.__name__, maximum_value_boundary))


@overload
def has_value_between() -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    maximum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    exclusive_minimum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    exclusive_maximum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
    exclusive_minimum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    maximum: Boundary[int],
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> AlwaysFailure[TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
    maximum: Boundary[int],
) -> Result[HasValueBetween, TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Result[HasValueBetween, TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    exclusive_minimum: Boundary[int],
    maximum: Boundary[int],
) -> Result[HasValueBetween, TestplatesError]:
    ...


@overload
def has_value_between(
    *,
    exclusive_minimum: Boundary[int],
    exclusive_maximum: Boundary[int],
) -> Result[HasValueBetween, TestplatesError]:
    ...


def has_value_between(
    *,
    minimum: Optional[Boundary[int]] = None,
    maximum: Optional[Boundary[int]] = None,
    exclusive_minimum: Optional[Boundary[int]] = None,
    exclusive_maximum: Optional[Boundary[int]] = None,
) -> Result[HasValueBetween, TestplatesError]:

    """
    Returns constraint object that matches any object with boundaries
    support that ranges between minimum and maximum boundaries values.

    :param minimum: inclusive minimum boundary value
    :param maximum: inclusive maximum boundary value
    :param exclusive_minimum: exclusive minimum boundary value
    :param exclusive_maximum: exclusive maximum boundary value
    """

    if (
        (minimum is UNLIMITED and maximum is UNLIMITED)
        or (minimum is UNLIMITED and exclusive_maximum is UNLIMITED)
        or (exclusive_minimum is UNLIMITED and maximum is UNLIMITED)
        or (exclusive_minimum is UNLIMITED and exclusive_maximum is UNLIMITED)
    ):
        return failure(UnlimitedRangeError())

    result = get_value_boundaries(
        inclusive_minimum=minimum,
        inclusive_maximum=maximum,
        exclusive_minimum=exclusive_minimum,
        exclusive_maximum=exclusive_maximum,
    )

    if not result:
        return result

    minimum_value_boundary, maximum_value_boundary = unwrap_success(result)

    return success(
        HasValueBetween(
            has_value_between.__name__,
            minimum_value=minimum_value_boundary,
            maximum_value=maximum_value_boundary,
        )
    )


def is_one_of(
    first: _GenericType,
    second: _GenericType,
    /,
    *rest: _GenericType,
) -> Result[IsOneOf[_GenericType], TestplatesError]:

    """
    Returns constraint object that matches any object
    which was specified via the positional arguments.

    :param first: first value to be matched by the constraint object
    :param second: second value to be matched by the constraint object
    :param rest: other values to be matched by constraint object
    """

    return success(IsOneOf(is_one_of.__name__, first, second, *rest))


def is_permutation_of(
    values: List[_GenericType],
    /,
) -> Result[IsPermutationOf[_GenericType], TestplatesError]:

    """
    Returns constraint object that matches any collection object
    that is a permutation of values specified via parameter.

    :param values: values to be matched as permutation
    """

    return success(IsPermutationOf(is_permutation_of.__name__, values))


def matches_pattern(
    pattern: AnyStr,
    /,
) -> Result[MatchesPattern[AnyStr], TestplatesError]:

    """
    Returns constraint object that matches any string
    object whose content matches the specified pattern.

    :param pattern: pattern to be matched inside string content
    """

    return success(MatchesPattern(matches_pattern.__name__, pattern))
