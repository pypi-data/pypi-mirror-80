from __future__ import annotations

__all__ = (
    "Field",
    "Structure",
    "StructureMeta",
    "StructureDict",
)

import abc
import testplates

from typing import (
    cast,
    overload,
    Any,
    TypeVar,
    Generic,
    ClassVar,
    Union,
    Tuple,
    Dict,
    Iterator,
    Mapping,
    Callable,
    Optional,
)

from resultful import (
    success,
    failure,
    Result,
)

from testplates.impl.utils import (
    format_like_dict,
)

from .value import (
    is_value,
    values_matches,
    SecretType,
    Maybe,
    Validator,
    ANY,
    WILDCARD,
    ABSENT,
    MISSING,
)

from .exceptions import (
    TestplatesError,
    MissingValueError,
    UnexpectedValueError,
    ProhibitedValueError,
)

_CovariantType = TypeVar("_CovariantType", covariant=True)


class Field(Generic[_CovariantType]):

    """
    Field descriptor class.
    """

    __slots__ = (
        "_validator",
        "_default",
        "_default_factory",
        "_optional",
        "_name",
    )

    def __init__(
        self,
        validator: Validator,
        /,
        *,
        default: Maybe[_CovariantType] = MISSING,
        default_factory: Maybe[Callable[[], _CovariantType]] = MISSING,
        optional: bool = False,
    ) -> None:
        self._validator = validator
        self._default = default
        self._default_factory = default_factory
        self._optional = optional

    def __repr__(self) -> str:
        parameters = [f"{self._name!r}"]

        if (default := self.default) is not MISSING:
            parameters.append(f"default={default!r}")

        parameters.append(f"optional={self.is_optional!r}")

        return f"{testplates.__name__}.{type(self).__name__}({', '.join(parameters)})"

    def __set_name__(
        self,
        owner: Callable[..., Structure],
        name: str,
    ) -> None:
        self._name = name

    @overload
    def __get__(
        self,
        instance: None,
        owner: Callable[..., Structure],
    ) -> Field[_CovariantType]:
        ...

    @overload
    def __get__(
        self,
        instance: Structure,
        owner: Callable[..., Structure],
    ) -> _CovariantType:
        ...

    # noinspection PyProtectedMember
    def __get__(
        self,
        instance: Optional[Structure],
        owner: Callable[..., Structure],
    ) -> Union[Field[_CovariantType], _CovariantType]:

        """
        Returns either field itself or field value.

        Return value depends on the fact whether field was accessed
        via :class:`Structure` class object or class instance attribute.

        :param instance: :class:`Structure` class instance to which field is attached or None
        :param owner: :class:`Structure` class object to which field is attached
        """

        if instance is None:
            return self

        return cast(_CovariantType, instance._testplates_values_[self.name])

    @property
    def name(self) -> str:

        """
        Returns field name.
        """

        return self._name

    @property
    def validator(self) -> Validator:

        """
        Returns field validator function.
        """

        return self._validator

    # noinspection PyCallingNonCallable
    @property
    def default(self) -> Maybe[_CovariantType]:

        """
        Returns field default value.

        If the field does not have a default value,
        missing value indicator is returned instead.
        """

        default_factory = self._default_factory

        if default_factory is not MISSING:
            return default_factory()

        return self._default

    @property
    def is_optional(self) -> bool:

        """
        Returns True if field is optional, otherwise False.
        """

        return self._optional

    # noinspection PyUnboundLocalVariable
    def validate(
        self,
        value: Maybe[_CovariantType],
        /,
    ) -> Result[None, TestplatesError]:

        """
        Validates the given value against the field requirements.

        :param value: value to be validated
        """

        default = self.default

        if value is ANY:
            return success(None)

        elif value is MISSING and default is MISSING:
            return failure(MissingValueError(self))

        elif (value is ABSENT or default is ABSENT) and not self.is_optional:
            return failure(ProhibitedValueError(self, value))

        elif (value is WILDCARD or default is WILDCARD) and not self.is_optional:
            return failure(ProhibitedValueError(self, value))

        elif is_value(value) and not (result := self.validator(value)):
            return result

        return success(None)


class StructureDict(Dict[str, Any]):

    __slots__ = ("fields",)

    def __init__(
        self,
        mapping: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        self.fields: Dict[str, Field[Any]] = {}

        for key, value in (mapping or kwargs).items():
            self[key] = value

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        if isinstance(value, Field):
            self.fields[key] = value

        super().__setitem__(key, value)


class StructureMeta(abc.ABCMeta):

    """
    Structure template metaclass.
    """

    __slots__ = ()

    _testplates_fields_: Mapping[str, Field[Any]]

    def __init__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: StructureDict,
    ) -> None:
        super().__init__(name, bases, attrs)

        cls._testplates_fields_ = attrs.fields

    def __repr__(self) -> str:
        parameters = format_like_dict(self._testplates_fields_)

        return f"{testplates.__name__}.{type(self).__name__}({parameters})"

    @classmethod
    def __prepare__(
        mcs,
        __name: str,
        __bases: Tuple[type, ...],
        **kwargs: Any,
    ) -> StructureDict:
        return StructureDict()

    def _testplates_create_(
        cls,
        name: str,
        **fields: Field[Any],
    ) -> StructureMeta:
        bases = (cls,)
        metaclass = cls.__class__

        attrs = metaclass.__prepare__(name, bases)

        for key, field in (fields or {}).items():
            attrs.__setitem__(key, field)

        instance = cast(StructureMeta, metaclass.__new__(metaclass, name, bases, attrs))
        metaclass.__init__(instance, name, bases, attrs)

        return instance


class Structure(Mapping[str, Any], metaclass=StructureMeta):

    """
    Structure template base class.
    """

    __slots__ = ("_testplates_values_",)

    # noinspection PyTypeChecker
    _testplates_self_ = TypeVar("_testplates_self_", bound="Structure")
    _testplates_fields_: ClassVar[Mapping[str, Field[Any]]]

    def __init__(
        self,
        __use_testplates_initialize_function_to_create_structure_not_init_method__: SecretType,
        /,
    ) -> None:
        self._testplates_values_: Mapping[str, Any] = {}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({format_like_dict(self._testplates_values_)})"

    def __getitem__(self, item: str) -> object:
        return self._testplates_values_[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._testplates_values_)

    def __len__(self) -> int:
        return len(self._testplates_values_)

    def __eq__(self, other: Any) -> bool:
        for key, field in self._testplates_fields_.items():
            self_value: Maybe[Any] = self._testplates_get_value_(self, key)
            other_value: Maybe[Any] = self._testplates_get_value_(other, key)

            if not values_matches(self_value, other_value):
                return False

        return True

    def _testplates_init_(
        self: _testplates_self_,
        **values: Any,
    ) -> Result[_testplates_self_, TestplatesError]:
        keys = self._testplates_fields_.keys()

        for key, value in values.items():
            if key not in keys:
                return failure(UnexpectedValueError(key, value))

        for key, field in self._testplates_fields_.items():
            if not (result := field.validate(values.get(key, MISSING))):
                return result

            if (default := field.default) is not MISSING:
                values.setdefault(key, default)

        self._testplates_values_ = values

        return success(self)

    # noinspection PyProtectedMember
    def _testplates_modify_(
        self: _testplates_self_,
        **values: Any,
    ) -> Result[_testplates_self_, TestplatesError]:
        typ = type(self)

        new_values: Dict[str, Any] = dict()
        new_values.update(self._testplates_values_)
        new_values.update(values)

        return typ(SecretType.SECRET)._testplates_init_(**new_values)

    @staticmethod
    def _testplates_get_value_(
        self: _testplates_self_,
        key: str,
        /,
        *,
        default: Maybe[_CovariantType] = MISSING,
    ) -> Maybe[_CovariantType]:

        """
        Extracts value by given key using a type specific protocol.

        If value is missing, returns default value.

        :param self: object with a type specific protocol
        :param key: key used to access the value in a structure
        :param default: default value that will be used in case value is missing
        """

        return self.get(key, default)
