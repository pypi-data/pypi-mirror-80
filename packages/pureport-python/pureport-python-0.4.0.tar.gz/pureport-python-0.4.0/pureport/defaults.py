# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
The Pureport defaults module holds all default values that are
used by various classes and functions..  This module provides
access to all defaults and exposes them as properties.  Some
properties can be customized with environment settings.
"""
from __future__ import absolute_import

import os
import sys

from collections import namedtuple

from pureport import transforms


ConfigItem = namedtuple('ConfigItem',
                        ('description', 'default', 'env', 'transform'))


def config_item(default, description=None, env=None, transform=None):
    transform = transform or transforms.to_str
    assert callable(transform), "transform must be a callable function"
    return ConfigItem(description, default, env, transform)


API_BASE_URL = config_item(
    description="Configures the base url to use for the Pureport API",
    default="https://api.pureport.com",
    env="PUREPORT_API_BASE_URL"
)


API_KEY = config_item(
    description="Returns the default Pureport API key",
    default=None,
    env="PUREPORT_API_KEY"
)


API_SECRET = config_item(
    description="Returns the default Pureport API secret",
    default=None,
    env="PUREPORT_API_SECRET"
)


CREDENTIALS_FILENAME = config_item(
    description="Name of the file to use for looking up credentials",
    default="credentials"
)


CREDENTIALS_PATH = config_item(
    description="Path that contains the credentials information",
    default=os.path.expanduser('~/.pureport'),
    env="PUREPORT_CREDENTIALS_PATH"
)


GENERIC_TRANSPORT_ERROR_MESSAGE = config_item(
    description="Generic error message string for pureport.transport",
    default=str(
        "unknown transport error occured, please review the caught "
        "exception for details"
    )
)


LOGGING_LEVEL = config_item(
    description="Set the logging level",
    default=0,
    transform=transforms.to_int,
    env="PUREPORT_LOGGING_LEVEL"
)


def defaults():
    attrs = {}
    for item in globals():
        obj = globals().get(item)
        if isinstance(obj, ConfigItem):
            name = item.lower()
            if obj.env:
                value = os.getenv(obj.env, obj.default)
            else:
                value = obj.default
            if value is not None:
                value = obj.transform(value)
            attrs[name] = value
    return namedtuple('Defaults', attrs)(**attrs)


sys.modules[__name__] = defaults()
