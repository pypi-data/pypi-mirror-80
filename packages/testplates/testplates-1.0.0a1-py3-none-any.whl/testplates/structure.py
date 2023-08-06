__all__ = (
    "struct",
    "create",
    "init",
    "modify",
    "fields",
    "field",
)

from typing import (
    cast,
    overload,
    Any,
    Type,
    TypeVar,
    Mapping,
    Callable,
)

from resultful import (
    Result,
)

from testplates.impl.base import (
    Field,
    Structure,
    StructureMeta,
    StructureDict,
    SecretType,
)

from .value import (
    Maybe,
    Validator,
    MISSING,
)

from .validators import (
    passthrough_validator,
)

from .exceptions import (
    TestplatesError,
)

_GenericType = TypeVar("_GenericType")
_StructureType = TypeVar("_StructureType", bound=Structure)


# noinspection PyTypeChecker
def struct(
    cls: Type[_GenericType],
    /,
) -> Type[Structure]:

    """
    Decorator API for creating structure.

    :param cls: structure base class
    """

    name = cls.__name__
    bases = (cls, Structure)
    attrs = StructureDict(cls.__dict__)

    return cast(Type[Structure], StructureMeta(name, bases, attrs))


# noinspection PyTypeChecker
# noinspection PyShadowingNames
# noinspection PyProtectedMember
def create(
    name: str,
    /,
    **fields: Field[Any],
) -> Type[Structure]:

    """
    Functional API for creating structure.

    :param name: structure type name
    :param fields: structure fields
    """

    return cast(Type[Structure], Structure._testplates_create_(name, **fields))


# noinspection PyProtectedMember
def init(
    structure_type: Type[_StructureType],
    /,
    **values: Any,
) -> Result[_StructureType, TestplatesError]:

    """
    Initializes structure with given values.

    :param structure_type: structure type
    :param values: structure initialization values
    """

    return structure_type(SecretType.SECRET)._testplates_init_(**values)


# noinspection PyProtectedMember
def modify(
    structure: _StructureType,
    /,
    **values: Any,
) -> Result[_StructureType, TestplatesError]:

    """
    Modifies structure with given values.

    :param structure: structure instance
    :param values: structure modification values
    """

    return structure._testplates_modify_(**values)


# noinspection PyProtectedMember
def fields(
    structure_type: Type[Structure],
    /,
) -> Mapping[str, Field[Any]]:

    """
    Returns structure fields.

    :param structure_type: structure type
    """

    return dict(structure_type._testplates_fields_)


@overload
def field(
    type: Type[_GenericType],
    validator: Validator = ...,
    /,
    *,
    optional: bool = ...,
) -> Field[_GenericType]:
    ...


@overload
def field(
    type: Type[_GenericType],
    validator: Validator = ...,
    /,
    *,
    default: _GenericType,
    optional: bool = ...,
) -> Field[_GenericType]:
    ...


@overload
def field(
    type: Type[_GenericType],
    validator: Validator = ...,
    /,
    *,
    default_factory: Callable[[], _GenericType],
    optional: bool = ...,
) -> Field[_GenericType]:
    ...


# noinspection PyUnusedLocal
def field(
    type: Type[_GenericType],
    validator: Validator = passthrough_validator,
    /,
    *,
    default: Maybe[_GenericType] = MISSING,
    default_factory: Maybe[Callable[[], _GenericType]] = MISSING,
    optional: bool = False,
) -> Field[_GenericType]:

    """
    Creates field for structure.

    This is basically a wrapper for :class:`Field`
    with all possible overloads for its arguments.

    :param type: field type
    :param validator: field validator function or None
    :param default: field default value
    :param default_factory: field default value factory
    :param optional: indication whether field is optional or not
    """

    return Field(validator, default=default, default_factory=default_factory, optional=optional)
