# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
The Pureport models module is reponsible for dynamically creating a set
objects based on the Pureport OpenAPI schema.  This module will read
the OpenAPI spec and generate classes for each model found in the
schema.

The models are used to calling bound API functions from the `pureport.api`
module.  Additionally, the models provide type checking of the input
values to ensure requests and responses are properly formatted.
"""
from __future__ import absolute_import

import sys
import logging

from keyword import iskeyword
from functools import partial
from functools import lru_cache

from pureport.transforms import to_snake_case
from pureport.transforms import to_str
from pureport.transforms import to_int
from pureport.transforms import to_bool
from pureport.transforms import to_list
from pureport.helpers import get_api
from pureport.helpers import get_value
from pureport.exceptions import PureportError
from pureport.session import Session
from pureport.credentials import default


log = logging.getLogger(__name__)


class Schema(object):

    def __init__(self, **kwargs):
        self._properties = kwargs

    type = property(lambda self: self._properties.get('type'))
    description = property(lambda self: self._properties.get('description'))


class Model(Schema):

    required = property(lambda self: self._properties.get('required', []))
    properties = property(lambda self: self._properties.get('properties', {}))
    base = property(lambda self: self._properties.get('base', ()))
    parents = property(lambda self: self._properties.get('parents', {}))
    discriminator = property(lambda self: self._properties.get('discriminator', {}))
    mapping = property(lambda self: self._properties.get('mapping', {}))


class Enum(Schema):

    values = property(lambda self: self._properties.get('enum', []))


def describe(model, readwrite=False, required=False):
    """Returns a complete data structure for a model

    This function accepts two filter keyword arguments for
    controlling the returned data structure.

    If the `readwrite` argument is set to True, then the response will
    only include fields that are read/write fields.  If set to
    False (default), then all fields are included.

    If the `required` argument is set to True, then the response will
    only include required fields to create a new object.  If the
    value is False (default), all fields are returned.

    :param model: the name of the model to construct
    :type model: str

    :param readwrite: filter the returned properties to readwrite fields only
    :type readwrite: bool

    :param required: filter the returned properties to only required fields
    :type required: bool

    :returns: a fully constructed object
    :rtype: dict
    """
    cls = globals().get(model)
    schema = cls._schema

    properties = {}

    if isinstance(schema, Model):
        for key, value in schema.parents.items():
            properties.update(describe(key, readwrite, required))

    if isinstance(schema, Enum):
        properties.update({
            'type': schema.type,
            'enum': schema.values,
        })
        return properties

    elif isinstance(schema, Model):
        for item in schema.properties:
            if readwrite is False or (readwrite is True and schema.properties[item].get('readOnly', False) is False):
                if not required or (required and item in schema.required):
                    if '$ref' in schema.properties[item]:
                        ref = schema.properties[item]['$ref'].split('/')[-1]
                        value = describe(ref, readwrite, required)

                        if 'enum' in value:
                            value.update({
                                'required': item in schema.required,
                                'readonly': schema.properties[item].get('readOnly', False),
                                'ref': ref
                            })
                            properties[item] = value

                        else:
                            properties[item] = {
                                'items': value,
                                'required': item in schema.required,
                                'readonly': schema.properties[item].get('readOnly', False),
                                'ref': ref,
                                'type': schema.properties[item].get('type', 'object')
                            }
                    else:
                        properties[item] = {
                            'type': schema.properties[item].get('type', 'string'),
                            'required': item in schema.required,
                            'readonly': schema.properties[item].get('readOnly', False)
                        }

    return properties


def dump(obj):
    """Deserialize model to a Python dict

    :param obj: an instance of `Model`
    :type obj: `pureport.models.Model`

    :returns: a Python dict object with camel case keys
    :rtype: dict
    """
    schema = obj._schema

    properties = {}
    mapping = {}

    for key, value in schema.parents.items():
        properties.update(value.properties)
        mapping.update(value.mapping)

    properties.update(schema.properties)
    mapping.update(schema.mapping)

    values = {}

    for key, value in properties.items():
        value = getattr(obj, key)

        if isinstance(value, Base):
            value = dump(value)

        if value is not None:
            values[mapping[key]] = value

    return values


def load(clsname, data):
    """Serialize data to an instance of Model

    :param clsname: the name of the model to create
    :type clsname: str

    :param data: key value data to load
    :type data: dict

    :returns: an instance of Model
    :rtype: `pureport.models.Model`
    """
    kwargs = {}

    model = globals().get(clsname)
    schema = model._schema
    properties = model._schema.properties

    data = dict([(to_snake_case(key), value) for key, value in data.items()])

    if schema.discriminator:
        value = data.get(schema.discriminator['propertyName'])
        if value:
            clsname = schema.discriminator['mapping'][value].split('/')[-1]
            schema = globals().get(clsname)._schema
            properties.update(schema.properties)

    for key, value in schema.parents.items():
        properties.update(value.properties)

    for key, value in properties.items():
        if data.get(key) is not None:
            if '$ref' in value:
                ref = value['$ref'].split('/')[-1]
                obj = globals().get(ref)._schema

                if isinstance(obj, Enum):
                    kwargs[key] = data[key]
                else:
                    kwargs[key] = load(ref, data[key])
            else:
                kwargs[key] = data[key]

    return globals().get(clsname)(**kwargs)


def load_api(data):
    schemas = data['components']['schemas']
    objects = dict()

    for name, schema in schemas.items():
        if 'allOf' in schema:
            model = {}
            for item in schema['allOf']:
                if '$ref' in item:
                    ref = item['$ref'].split('/')[-1]
                    if 'base' not in model:
                        model['base'] = list()
                    model['base'].append(ref)

                elif 'properties' in item:
                    model['properties'] = item['properties']

            schema.update(model)

            del schema['allOf']

        if 'properties' in schema:
            model = {}
            mapping = {}

            for key, value in schema['properties'].items():
                new_key = to_snake_case(key)
                model[new_key] = value
                mapping[new_key] = key

            schema['properties'] = model
            schema['mapping'] = mapping

            if 'required' in schema:
                schema['required'] = [to_snake_case(v) for v in schema['required']]

            objects[name] = Model(**schema)

        elif 'enum' in schema:
            objects[name] = Enum(**schema)

        schemas[name] = schema
    return objects


class Array(object):

    def __init__(self, cls):
        self.cls = cls
        self._items = list()

    def __repr__(self):
        return str(self._items)

    def __validate__(self, value):
        if isinstance(value, dict):
            value = load(self.cls.__name__, value)
        if not isinstance(value, self.cls):
            raise PureportError("invalid value type")
        return value

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = self.__validate__(value)

    def __delitem__(self, index):
        del self._items[index]

    def __contains__(self, value):
        return value in self._items

    def __iter__(self):
        return iter(self._items)

    def __iadd__(self, other):
        self._items.expand(other)

    def __reversed__(self):
        return self._items.reversed()

    def __len__(self):
        return len(self._items)

    def insert(self, index, value):
        self._items[index] = self.__validate__(value)

    def index(self, value):
        return self._items.index(value)

    def count(self, value):
        return self._items.count(value)

    def append(self, value):
        self._items.append(self.__validate__(value))

    def reverse(self):
        self._items.reverse()

    def extend(self, value):
        value = [self.__validate__(v) for v in value]
        self._items.extend(value)

    def pop(self, index):
        self._items.pop(index)

    def remove(self, value):
        self._items.remove(value)

    def serialize(self):
        return [o.serialize() for o in self._items]


def _get_property(self, name):
    if name in self.__dict__:
        return self.__dict__[name]
    else:
        prop = self._schema.properties.get(name)
        if prop is None and self._schema.base:
            for item in self._schema.base:
                prop = self._schema.parents[item].properties.get(name)
                if prop:
                    break
        return prop.get('default')


def _delete_property(self, name):
    if name in self.__dict__:
        del self.__dict__[name]


def _set_property(self, value, name):
    val = None

    this = self._schema.properties.get(name)

    if this is None and self._schema.base:
        for item in self._schema.base:
            this = self._schema.parents[item].properties.get(name)
            if this:
                break
        else:
            raise KeyError(name)

    if this is None:
        raise KeyError(name)

    if '$ref' in this:
        ref = this['$ref'].split('/')[-1]
        schema = globals().get(ref)._schema

        if isinstance(schema, Model):
            if schema.discriminator:
                prop = getattr(value, schema.discriminator['propertyName'])
                ref = schema.discriminator['mapping'][prop].split('/')[-1]

            clstype = globals().get(ref)

            if value is not None and not isinstance(value, clstype):
                raise TypeError("invalid object type")

            val = value

        elif isinstance(schema, Enum):
            if value is not None:
                value = value.upper() if schema.type == 'string' else value
                if value not in schema.values:
                    raise ValueError("invalid enum value")
                val = value

        else:
            val = value

    else:
        value = this.get('default') if value is None else value

        if value is not None:
            if this.get('type') == 'string':
                maxlen = this.get('maxLength') or sys.maxsize
                minlen = this.get('minLength') or 0
                val = to_str(value, minlen, maxlen)

            elif this.get('type') == 'boolean':
                val = to_bool(value)

            elif this.get('type') == 'integer':
                minimum = this.get('minimum')
                maximum = this.get('maximum')
                val = to_int(value, minimum, maximum)

            elif this.get('type') == 'array':
                if not isinstance(value, (list, set, tuple, dict)):
                    raise ValueError("invalid value for type <array>")

                if this.get('items') and '$ref' in this['items']:
                    clsname = this['items']['$ref'].split('/')[-1]
                    val = Array(globals().get(clsname))
                    for item in value:
                        val.append(load(clsname, item))
                elif this.get('items') and 'type' in this['items']:
                    item_type = this['items']['type']
                    if item_type == 'string':
                        val = [to_str(v) for v in value]
                    elif item_type == 'integer':
                        val = [to_int(v) for v in value]
                    else:
                        val = to_list(value)
                else:
                    val = to_list(value)

                if this.get('uniqueItems') is True:
                    val = list(set(val))

            elif this.get('type') == 'object':
                if not isinstance(value, dict):
                    raise ValueError("value must be of type <dict>")
                val = value

            else:
                val = value

    self.__dict__[name] = val


class Base(object):

    def __init__(self, *args, **kwargs):
        if self._schema.required:
            required_args = self._schema.required.copy()

            for item in self._schema.required:
                if item in kwargs:
                    required_args.remove(item)

            if required_args and len(required_args) != len(args):
                raise TypeError(str(
                    "__init__() missing {} required positional arguments: "
                    "{}".format(len(required_args), ', '.join(required_args)))
                )

            kwargs.update(dict(zip(required_args, args)))

        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                self.__dict__[key] = value

    def update(self, data):
        """Update the model with new values
        """
        for key, value in data.items():
            if isinstance(getattr(self, key), Base):
                model = describe(self.__class__.__name__)
                value = load(model[key]['ref'], value)
            setattr(self, key, value)

    def serialize(self):
        """Serialize the object to a dict

        All properties will be serialized to key value pairs using
        the currenty property name in snake case.  If you need to
        serialize the object to camel case names, use the `dump`
        function instead.

        :returns: a dict object that presents the instance
        :rtype: dict
        """
        obj = {}
        for key, value in self.__dict__.items():
            if isinstance(value, (Base, Array)):
                obj[key] = value.serialize()
            elif isinstance(value, list) and len(value):
                if isinstance(value[0], Base):
                    obj[key] = [v.serialize() for v in value]
                else:
                    obj[key] = value
            else:
                obj[key] = value
        return obj


class StrictBase(Base):

    def __init__(self, *args, **kwargs):
        super(StrictBase, self).__init__(*args, **kwargs)
        for item in self._schema.required:
            if getattr(self, item) is None:
                msg = str("missing value for required property `{}.{}`").format(
                    self.__class__.__name__,
                    item
                )
                raise ValueError(msg)


@lru_cache(maxsize=16)
def make(session=None):
    log.debug("generating bindings for models")

    session = session or Session(*default())

    schemas = get_api(session)
    globals()['__version__'] = get_value('info.version', schemas)

    schemas = load_api(schemas)
    models = list()

    for name, schema in schemas.items():
        if iskeyword(name):
            raise PureportError("`{}` is a reserved keyword".format(name))

        if isinstance(schema, Enum):
            attrs = {}
            for index, item in enumerate(schema.values):
                attrs[str(item)] = index
            attrs['_schema'] = schema
            globals()[name] = type(name, (object,), attrs)

        if isinstance(schema, Model):
            properties = {}
            for item in schema.base:
                properties.update(schemas[item].properties)
            properties.update(schema.properties)

            props = {}

            for key, value in properties.items():
                if iskeyword(key):
                    raise PureportError("`{}` property name is a reserved keyword".format(key))

                kwargs = {
                    'fget': partial(_get_property, name=key),
                    'doc': value.get('description', 'UNDEFINED')
                }

                if value.get('readOnly') is not True:
                    kwargs.update({
                        'fset': partial(_set_property, name=key),
                        'fdel': partial(_delete_property, name=key)
                    })

                props[key] = property(**kwargs)

            props['_schema'] = schema
            log.debug("adding model {}".format(name))
            cls = type(name, (StrictBase,), props)
            models.append(name)
            globals()[name] = cls

    # this will iterate back over all of the models at attach parent schemas to
    # the model instance.  this allows for the entire model to be
    # reconstructured later.
    for item in models:
        schema = globals().get(item)._schema
        parents = dict([(item, globals().get(item)._schema) for item in schema.base])
        schema._properties['parents'] = parents
