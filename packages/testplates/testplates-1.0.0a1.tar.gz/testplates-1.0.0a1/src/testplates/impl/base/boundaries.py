__all__ = (
    "get_minimum_value",
    "get_maximum_value",
    "get_minimum_size",
    "get_maximum_size",
    "get_value_boundaries",
    "get_size_boundaries",
    "fits_minimum_value",
    "fits_maximum_value",
    "fits_minimum_size",
    "fits_maximum_size",
)

import sys

from typing import (
    Sized,
    Tuple,
    Union,
    Optional,
    Final,
)

from resultful import (
    success,
    failure,
    unwrap_success,
    Result,
)

from .value import (
    UnlimitedType,
    UNLIMITED,
)

from .limit import (
    Limit,
    Extremum,
    MINIMUM_EXTREMUM,
    MAXIMUM_EXTREMUM,
)

from .exceptions import (
    TestplatesError,
    MissingBoundaryError,
    InvalidSizeError,
    MutuallyExclusiveBoundariesError,
    OverlappingBoundariesError,
    SingleMatchBoundariesError,
)

Edge = Union[int, UnlimitedType]
Boundary = Union[Limit, UnlimitedType]

SIZE_MINIMUM: Final[int] = 0
SIZE_MAXIMUM: Final[int] = sys.maxsize


def get_minimum_value(
    inclusive: Optional[Edge] = None,
    exclusive: Optional[Edge] = None,
    ignore_unlimited: bool = False,
) -> Result[Boundary, TestplatesError]:

    """
    Gets minimum boundary.

    :param inclusive: inclusive boundary value or None
    :param exclusive: exclusive boundary value or None
    :param ignore_unlimited: indicates whether to ignore unlimited values or not
    """

    return get_value_boundary(
        MINIMUM_EXTREMUM,
        inclusive=inclusive,
        exclusive=exclusive,
        ignore_unlimited=ignore_unlimited,
    )


def get_maximum_value(
    inclusive: Optional[Edge] = None,
    exclusive: Optional[Edge] = None,
    ignore_unlimited: bool = False,
) -> Result[Boundary, TestplatesError]:

    """
    Gets maximum boundary.

    :param inclusive: inclusive boundary value or None
    :param exclusive: exclusive boundary value or None
    :param ignore_unlimited: indicates whether to ignore unlimited values or not
    """

    return get_value_boundary(
        MAXIMUM_EXTREMUM,
        inclusive=inclusive,
        exclusive=exclusive,
        ignore_unlimited=ignore_unlimited,
    )


def get_minimum_size(
    size: Edge,
    /,
) -> Result[Boundary, TestplatesError]:

    """
    Gets minimum size boundary.

    :param size: inclusive boundary value or None
    """

    if size is UNLIMITED:
        return success(size)

    boundary = Limit(MINIMUM_EXTREMUM, size, is_inclusive=True)

    if is_outside_size_range(boundary):
        return failure(InvalidSizeError(boundary))

    return success(boundary)


def get_maximum_size(
    size: Edge,
    /,
) -> Result[Boundary, TestplatesError]:

    """
    Gets maximum size boundary.

    :param size: inclusive boundary value or None
    """

    if size is UNLIMITED:
        return success(size)

    boundary = Limit(MAXIMUM_EXTREMUM, size, is_inclusive=True)

    if is_outside_size_range(boundary):
        return failure(InvalidSizeError(boundary))

    return success(boundary)


def get_value_boundary(
    name: Extremum,
    *,
    inclusive: Optional[Edge] = None,
    exclusive: Optional[Edge] = None,
    ignore_unlimited: bool = False,
) -> Result[Boundary, TestplatesError]:

    """
    Gets boundary.

    :param name: extremum name
    :param inclusive: inclusive boundary value or None
    :param exclusive: exclusive boundary value or None
    :param ignore_unlimited: indicates whether to ignore unlimited values or not
    """

    if inclusive is None and exclusive is None:
        return failure(MissingBoundaryError(name))

    if inclusive is not None and exclusive is not None:
        at_least_one_is_unlimited = inclusive is UNLIMITED or exclusive is UNLIMITED

        if not ignore_unlimited or (ignore_unlimited and not at_least_one_is_unlimited):
            return failure(MutuallyExclusiveBoundariesError(name))

    if inclusive is not None and inclusive is not UNLIMITED:
        return success(Limit(name, inclusive, is_inclusive=True))

    if exclusive is not None and exclusive is not UNLIMITED:
        return success(Limit(name, exclusive, is_inclusive=False))

    return success(UNLIMITED)


def get_value_boundaries(
    inclusive_minimum: Optional[Edge] = None,
    inclusive_maximum: Optional[Edge] = None,
    exclusive_minimum: Optional[Edge] = None,
    exclusive_maximum: Optional[Edge] = None,
    ignore_unlimited: bool = False,
) -> Result[Tuple[Boundary, Boundary], TestplatesError]:

    """
    Gets minimum and maximum value boundaries.

    :param inclusive_minimum: inclusive minimum boundary value
    :param inclusive_maximum: inclusive maximum boundary value
    :param exclusive_minimum: exclusive minimum boundary value
    :param exclusive_maximum: exclusive maximum boundary value
    :param ignore_unlimited: indicates whether to ignore unlimited values or not
    """

    minimum_result = get_minimum_value(
        inclusive=inclusive_minimum,
        exclusive=exclusive_minimum,
        ignore_unlimited=ignore_unlimited,
    )

    if not minimum_result:
        return failure(minimum_result)

    maximum_result = get_maximum_value(
        inclusive=inclusive_maximum,
        exclusive=exclusive_maximum,
        ignore_unlimited=ignore_unlimited,
    )

    if not maximum_result:
        return failure(maximum_result)

    minimum = unwrap_success(minimum_result)
    maximum = unwrap_success(maximum_result)

    result = validate_boundaries(minimum=minimum, maximum=maximum)

    if not result:
        return failure(result)

    return success((minimum, maximum))


def get_size_boundaries(
    inclusive_minimum: Edge,
    inclusive_maximum: Edge,
) -> Result[Tuple[Boundary, Boundary], TestplatesError]:

    """
    Gets minimum and maximum size boundaries.

    :param inclusive_minimum: inclusive minimum boundary value
    :param inclusive_maximum: inclusive maximum boundary value
    """

    minimum_result = get_minimum_size(inclusive_minimum)

    if not minimum_result:
        return failure(minimum_result)

    maximum_result = get_maximum_size(inclusive_maximum)

    if not maximum_result:
        return failure(maximum_result)

    minimum = unwrap_success(minimum_result)
    maximum = unwrap_success(maximum_result)

    result = validate_boundaries(minimum=minimum, maximum=maximum)

    if not result:
        return failure(result)

    return success((minimum, maximum))


def validate_boundaries(
    minimum: Boundary,
    maximum: Boundary,
) -> Result[None, TestplatesError]:

    """
    Checks minimum and maximum boundaries.

    :param minimum: minimum boundary
    :param maximum: maximum boundary
    """

    if minimum is UNLIMITED or maximum is UNLIMITED:
        return success(None)

    if is_overlapping(minimum, maximum):
        return failure(OverlappingBoundariesError(minimum, maximum))

    if is_single_match(minimum, maximum):
        return failure(SingleMatchBoundariesError(minimum, maximum))

    return success(None)


def is_outside_size_range(
    boundary: Limit,
) -> bool:

    """
    Returns True if boundary is outside of size range, otherwise False.

    :param boundary: boundary limit
    """

    return boundary.value < SIZE_MINIMUM or boundary.value > SIZE_MAXIMUM


def is_overlapping(
    minimum: Limit,
    maximum: Limit,
) -> bool:

    """
    Returns True if boundaries are overlapping each other, otherwise False.

    :param minimum: minimum boundary limit
    :param maximum: maximum boundary limit
    """

    return minimum.value + minimum.alignment > maximum.value - maximum.alignment


def is_single_match(
    minimum: Limit,
    maximum: Limit,
) -> bool:

    """
    Returns True if boundaries will match only single value, otherwise False.

    :param minimum: minimum boundary limit
    :param maximum: maximum boundary limit
    """

    return minimum.value + minimum.alignment == maximum.value - maximum.alignment


def fits_minimum_value(
    value: int,
    minimum: Boundary,
) -> bool:

    """
    Checks whether value fits the minimum boundary.

    :param value: value to be checked against boundary
    :param minimum: minimum boundary
    """

    if minimum is UNLIMITED:
        return True

    if minimum.is_inclusive:
        return value.__ge__(minimum.value) is True
    else:
        return value.__gt__(minimum.value) is True


def fits_maximum_value(
    value: int,
    maximum: Boundary,
) -> bool:

    """
    Checks whether value fits the maximum boundary.

    :param value: value to be checked against boundary
    :param maximum: maximum boundary
    """

    if maximum is UNLIMITED:
        return True

    if maximum.is_inclusive:
        return value.__le__(maximum.value) is True
    else:
        return value.__lt__(maximum.value) is True


def fits_minimum_size(
    value: Sized,
    minimum: Boundary,
) -> bool:

    """
    Checks whether value size fits the minimum boundary.

    :param value: value to be checked against boundary
    :param minimum: minimum boundary
    """

    return fits_minimum_value(len(value), minimum)


def fits_maximum_size(
    value: Sized,
    maximum: Boundary,
) -> bool:

    """
    Checks whether value size fits the maximum boundary.

    :param value: value to be checked against boundary
    :param maximum: maximum boundary
    """

    return fits_maximum_value(len(value), maximum)
