# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import random
import string
import tempfile
import shutil

from contextlib import contextmanager


@contextmanager
def tempdir():
    try:
        tmpdir = tempfile.mkdtemp()
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def random_string(nodigits=False, min=3, max=20):
    if nodigits is True:
        return ''.join(
            random.choice(string.ascii_uppercase) for _ in range(random.randint(min, max))
        )
    else:
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(min, max))
        )


def random_int(min=0, max=101):
    return random.randrange(min, max)


def random_float():
    return random.uniform(1.0, 100.0)
