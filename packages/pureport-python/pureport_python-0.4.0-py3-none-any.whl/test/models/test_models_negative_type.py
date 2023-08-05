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
        ModelData("Network", type="Network", name="", remove=True),
        ModelData("Connection", type="AWS_DIRECT_CONNECT", name="", remove=True),
        ModelData("Connection", type="AWS_DIRECT_CONNECT", speed="", remove=True),
        ModelData(
            "Connection", type="AWS_DIRECT_CONNECT", billing_term="HOURLY", remove=True
        ),
        ModelData(
            "Connection",
            type="AWS_DIRECT_CONNECT",
            high_availability="HOURLY",
            remove=True,
        ),
        ModelData("Connection", type="AWS_DIRECT_CONNECT", location="", remove=True),
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

    with pytest.raises(TypeError):
        models.load(model.type, model.data)
