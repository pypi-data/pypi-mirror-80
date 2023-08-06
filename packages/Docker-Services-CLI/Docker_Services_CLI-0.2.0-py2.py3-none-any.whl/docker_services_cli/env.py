# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Environment module."""

import os
import sys
from distutils.version import StrictVersion

import click

from .config import DEFAULT_VERSIONS, SERVICES


def _set_default_env(services_version, default_version):
    """Set environmental variable value if it does not exist."""
    os.environ[services_version] = os.environ.get(
        services_version, default_version
    )


def _is_version(version):
    """Checks if a string is a version of the format `x.y.z`.

    NOTE: It is not mandatory to be up to patch level. The following would be accepted:
    - 10.1
    - 9
    - 15.0.1a2
    """
    try:
        # StrictVersion fails on plain numbers (e.g. "10")
        if version.isnumeric():
            return True
        StrictVersion(version)
        return True
    except Exception:
        return False


def _load_or_set_env(services_version, default_version):
    """Set a specific service version from the environment.

    It parses the value to distinguish between a version and a defined latest.
    NOTE: It requires that all variables for latest versions have been set up.
    """
    version_from_env = os.environ.get(services_version, default_version)
    # e.g. the ES_7_LATEST string from env, need a second get.
    major_version_from_env = os.environ.get(version_from_env)

    if not version_from_env:
        os.environ[services_version] = default_version

    elif _is_version(version_from_env):
        os.environ[services_version] = version_from_env

    elif major_version_from_env and _is_version(major_version_from_env):
        os.environ[services_version] = major_version_from_env

    else:
        click.secho(
            f"Environment variable for version {version_from_env} not set \
            or set to a non-compliant format (dot separated numbers).", fg="red"
        )
        sys.exit(1)



def set_env():
    """Export the environment variables for services and versions."""
    # export variables for latest versions
    for key, value in DEFAULT_VERSIONS.items():
        _set_default_env(key, value)

    # export services configuration
    for service in SERVICES:
        for key, value in service.items():
            if key.endswith('_VERSION'):
                _load_or_set_env(key, value)
            else:
                _set_default_env(key, value)
