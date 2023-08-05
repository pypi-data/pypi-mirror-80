# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
#
"""
The query model provides a set of convience functions for querying
the Pureport API to find objects.  It supplements the functions
provided by `pureport.api` with a set of functions that can look
up objects based on different match criteria.

For instance, in order to get a network object, the `pureport.api`
module exposes a function `get_network()`.  The `get_network()`
function will return a `pureport.models.Network` object (if it
exists) based on the required argument `network_id`.  Since the
value of `network_id` is not immediately known, we can lookup
the value based on the network name.
"""

from functools import (
    partial,
    update_wrapper
)

from pureport.helpers import first
from pureport.exceptions import PureportError


def find_object(func, name, *args, **kwargs):
    """Locate an object by name or identifier

    This function will use the `name` argumetn to attempt to
    locate an object.  It will first attempt to find the
    object by identifier and if that fails, it will attempt
    to find the object by name.

    Since object names are non-unique values in the Pureport
    API, this function will return the first value it finds in the
    case of multiple objects.

    If the requested object can not be found, this function
    will raise an exception.

    :param name: The name or identifier of the object to locate
    :type name: str

    :returns: An instance of the object found
    :rtype: `pureport.models.Model`

    :raises: `pureport.exceptions.PureportError`
    """
    objects = func(*args, **kwargs)

    match = None
    name_matches = list()

    for item in objects:
        if name == item.id:
            match = item
            break
        elif name == item.name:
            name_matches.append(item)
    else:
        if not name_matches:
            raise PureportError("could not locate object `{}`".format(name))

    if match is None:
        match = first(name_matches)

    return match


def make(session):
    for f in ('find_connections', 'find_networks'):
        if not hasattr(session, f):
            raise PureportError(
                "cannot bind query function, missing {}".format(f)
            )

    find_connection = partial(find_object, session.find_connections)
    update_wrapper(find_connection, find_object)
    setattr(session, 'find_connection', find_connection)

    find_network = partial(find_object, session.find_networks)
    update_wrapper(find_network, find_object)
    setattr(session, 'find_network', find_network)
