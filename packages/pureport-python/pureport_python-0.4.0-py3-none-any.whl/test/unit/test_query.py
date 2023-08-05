# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved
#
from collections import namedtuple

from unittest.mock import Mock

import pytest

from ..utils import utils

from pureport import query
from pureport.session import Session
from pureport.exceptions import PureportError


Item = namedtuple('Item', ('id', 'name'))


def function():
    items = list()
    for i in range(0, 10):
        items.append(Item(i, 'item{}'.format(i)))
    return items


def test_find_object_by_id():
    resp = query.find_object(function, 5)
    assert resp.id == 5
    assert resp.name == 'item5'


def test_find_object_by_name():
    resp = query.find_object(function, 'item5')
    assert resp.id == 5
    assert resp.name == 'item5'


def test_find_object_raises_exception():
    with pytest.raises(PureportError):
        query.find_object(function, utils.random_string())


def test_query_functions_exist():
    session = Mock(spec=Session)

    session.find_connections = lambda self: []
    session.find_networks = lambda self: []

    assert not hasattr(session, 'find_network')
    assert not hasattr(session, 'find_connection')

    query.make(session)

    assert hasattr(session, 'find_network')
    assert callable(session.find_network)

    assert hasattr(session, 'find_connection')
    assert callable(session.find_connection)
