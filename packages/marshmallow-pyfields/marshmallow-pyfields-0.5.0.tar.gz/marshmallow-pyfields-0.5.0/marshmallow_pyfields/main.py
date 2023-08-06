#  Authors: Sylvain MARIE <sylvain.marie@se.com>
#           + All contributors to <https://github.com/smarie/python-marshmallow-pyfields>
#
#  License: 3-clause BSD, <https://github.com/smarie/python-marshmallow-pyfields/blob/master/LICENSE>

from functools import lru_cache
from typing import (
    Optional,
    Set,
    Tuple,
    Type,
    cast,
)

import marshmallow
from marshmallow_dataclass import field_for_schema, _base_schema

from pyfields import get_fields, Field


MAX_CLASS_SCHEMA_CACHE_SIZE = 1024
"""Max number of generated schemas that class_schema keeps of generated schemas. Removes duplicates."""

# Whitelist of dataclass members that will be copied to generated schema.
MEMBERS_WHITELIST: Set[str] = {"Meta"}


def get_schema(
        clazz: type,
        base_schema: Optional[Type[marshmallow.Schema]] = None
) -> Type[marshmallow.Schema]:
    """
    Convert a class using pyfields to a marshmallow schema. Strongly inspired by marshmallow_dataclass.class_schema.

    Note: TODO there is currently no way to pass custom marshmallow arguments or marshmallow fields.

    :param clazz: A python class using pyfields
    :param base_schema: marshmallow schema used as a base class when deriving the class schema
    :return: A marshmallow Schema corresponding to the class
    """
    return _possibly_cached_class_schema(clazz, base_schema)


@lru_cache(maxsize=MAX_CLASS_SCHEMA_CACHE_SIZE)
def _possibly_cached_class_schema(
    clazz: type, base_schema: Optional[Type[marshmallow.Schema]] = None
) -> Type[marshmallow.Schema]:

    # any pyfields fields ?
    fields: Tuple[Field] = get_fields(clazz)
    if len(fields) == 0:
        raise TypeError(
            f"{getattr(clazz, '__name__', repr(clazz))} has no fields."
        )

    # Copy all marshmallow hooks and whitelisted members of the dataclass to the schema.
    attributes = {
        k: v
        for k, v in vars(clazz).items()  # inspect.getmembers(clazz)
        if hasattr(v, "__marshmallow_hook__") or k in MEMBERS_WHITELIST
    }

    # Update the schema members to contain marshmallow fields instead of dataclass fields
    attributes.update(
        (
            field.name,
            field_for_schema(
                field.type_hint,
                marshmallow.missing if field.is_mandatory else field.default,
                None,  # field.metadata,
                base_schema
            ),
        )
        for field in fields
        # if field.init   TODO what is this for ?
    )

    schema_class = type(clazz.__name__, (_base_schema(clazz, base_schema),), attributes)
    return cast(Type[marshmallow.Schema], schema_class)
