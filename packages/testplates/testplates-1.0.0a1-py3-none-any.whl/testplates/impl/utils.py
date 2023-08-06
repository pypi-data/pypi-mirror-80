__all__ = (
    "format_like_tuple",
    "format_like_dict",
)

from typing import (
    Any,
    Iterable,
    Mapping,
)


def format_like_tuple(
    values: Iterable[Any],
) -> str:

    """
    Formats iterable into tuple-like format
    that is readable for human being.

    :param values: values to be formatted
    """

    return ", ".join((repr(value) for value in values))


def format_like_dict(
    mapping: Mapping[Any, Any],
) -> str:

    """
    Formats mapping into dict-like format
    that is readable for human being.

    :param mapping: values to be formatted
    """

    return ", ".join((f"{key}={value!r}" for key, value in mapping.items()))
