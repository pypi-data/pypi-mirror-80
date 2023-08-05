# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import os
import json

from unittest.mock import patch, Mock

from ..utils import utils

from pureport import models


def make_schema():
    return {
        "TestSchema": {
            "properties": {
                "camelCase": {
                    "type": "string"
                },
                "snake_case": {
                    "type": "string"
                }
            }
        }
    }


@patch.object(models, 'get_api')
def test_models_make(mock_get_api):
    basepath = os.path.dirname(__file__)

    content = json.loads(
        open(os.path.join(basepath, '../openapi.json')).read()
    )

    mock_get_api.return_value = content

    session = Mock()

    models.make(session)
    assert set(content['components']['schemas']).issubset(dir(models))


@patch.object(models, 'get_api')
def test_models_dump(mock_get_api):
    content = {'components': {'schemas': make_schema()}}
    mock_get_api.return_value = content

    session = Mock()
    models.make(session)

    assert hasattr(models.TestSchema, 'camel_case')
    assert hasattr(models.TestSchema, 'snake_case')

    camel_case_value = utils.random_string()
    snake_case_value = utils.random_string()

    obj = models.TestSchema(
        camel_case=camel_case_value, snake_case=snake_case_value
    )

    resp = models.dump(obj)

    assert resp['camelCase'] == camel_case_value
    assert resp['snake_case'] == snake_case_value

    delattr(models, 'TestSchema')


@patch.object(models, 'get_api')
def test_models_load(mock_get_api):
    camel_case_value = utils.random_string()
    snake_case_value = utils.random_string()

    content = {'components': {'schemas': make_schema()}}
    mock_get_api.return_value = content

    session = Mock()
    models.make(session)

    data = {'camel_case': camel_case_value, 'snake_case': snake_case_value}
    resp = models.load('TestSchema', data)

    assert isinstance(resp, models.TestSchema)
    assert resp.camel_case == camel_case_value
    assert resp.snake_case == snake_case_value
