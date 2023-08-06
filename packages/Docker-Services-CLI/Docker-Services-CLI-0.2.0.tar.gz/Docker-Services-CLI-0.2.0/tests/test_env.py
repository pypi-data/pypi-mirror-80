# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

import os

import pytest

from docker_services_cli.env import _is_version, _load_or_set_env


def test_is_version():
    assert _is_version("10")
    assert _is_version("10.1")
    assert _is_version("10.1.2")
    assert _is_version("10.1.2a3")
    assert not _is_version("SERVICE_10_LATEST")


def test_load_or_set_env_default():
    """Tests the loading of a given default value."""
    _load_or_set_env("TEST_VERSION_DEFAULT", "1.0.0")

    assert os.environ.get("TEST_VERSION_DEFAULT") == "1.0.0"

    del os.environ['TEST_VERSION_DEFAULT']


def test_load_or_set_env_from_value():
    """Tests the loading of a set value."""
    os.environ["TEST_VERSION_DEFAULT"] = "2.0.0"
    _load_or_set_env("TEST_VERSION_DEFAULT", "1.0.0")

    assert os.environ.get("TEST_VERSION_DEFAULT") == "2.0.0"

    del os.environ['TEST_VERSION_DEFAULT']

def test_load_or_set_env_from_string():
    """Tests the loading of a service default value from string."""
    os.environ["TEST_SERVICE_VERSION_DEFAULT"] = "1.0.0"
    os.environ["TEST_VERSION_DEFAULT"] = "TEST_SERVICE_VERSION_DEFAULT"
    _load_or_set_env("TEST_VERSION_DEFAULT", "2.0.0")

    assert os.environ.get("TEST_VERSION_DEFAULT") == "1.0.0"

    del os.environ['TEST_SERVICE_VERSION_DEFAULT']
    del os.environ['TEST_VERSION_DEFAULT']

def test_setversion_not_set():
    """Tests the loading when it results in a system exit."""
    os.environ["TEST_VERSION_DEFAULT"] = "TEST_NOT_EXISTING"

    with pytest.raises(SystemExit) as ex:
        _load_or_set_env("TEST_VERSION_DEFAULT", "2.0.0")

    assert ex.value.code == 1

    del os.environ['TEST_VERSION_DEFAULT']
