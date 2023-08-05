# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import pytest
import json
import os
from unittest.mock import patch, Mock
from pureport import models
from .test_helpers import ModelData


@pytest.mark.parametrize(
    "model",
    [
        ModelData("Connection", type="AWS_DIRECT_CONNECT", speed=150),
        ModelData("Connection", type="AWS_DIRECT_CONNECT", billing_term="None"),
    ],
)
@patch.object(models, 'get_api')
def test_model_load_exception(mock_get_api, model):
    basepath = os.path.dirname(__file__)
    content = json.loads(
        open(os.path.join(basepath, '../openapi.json')).read()
    )
    mock_get_api.return_value = content
    session = Mock()
    models.make(session)

    with pytest.raises(ValueError):
        models.load(model.type, model.data)
