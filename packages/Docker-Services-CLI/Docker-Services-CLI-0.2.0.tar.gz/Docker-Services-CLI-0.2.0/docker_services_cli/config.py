# -*- coding: utf-8 -*-
#
# Copyright (C 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration module.

Configuration values (e.g. service configuration) need to be set through
environment variables. However, sane defaults are provided below.

The list of services to be configured is taken from ``SERVICES``. Each one
should contain a ``<SERVICE_NAME>_VERSION`` varaible.

Service's version are treated slightly different:

- If the variable is not found in the environment, it will use the set default.
- If the variable is set with a version number (e.g. 10, 10.7) it will use
  said value.
- If the variable is set with a string point to one of the configured
  ``latests`` it will load the value of said ``latest`` and use it.

This means that the environment set/load logic will first set the default
versions before loading a given service's version.
"""

DOCKER_SERVICES_FILEPATH = "docker_services_cli/docker-services.yml"
"""Docker services file default path."""

DEFAULT_VERSIONS = {
    "ES_6_LATEST": "6.8.12",
    "ES_7_LATEST": "7.9.0",
    "POSTGRESQL_9_LATEST": "9.6.19",
    "POSTGRESQL_10_LATEST": "10.14",
    "POSTGRESQL_11_LATEST": "11.9",
    "POSTGRESQL_12_LATEST": "12.4",
    "POSTGRESQL_13_LATEST": "13.0",
    "MYSQL_5_LATEST": "5.7.31",
    "MYSQL_8_LATEST": "8.0.21",
    "REDIS_6_LATEST": "6.0.6",
    "MEMCACHED_LATEST": "1.6.6",
    "RABBITMQ_3_LATEST": "3.8.7",
}
"""Services default latest versions."""

# Elasticsearch
ELASTICSEARCH = {
    "ES_VERSION": "ES_7_LATEST"
}
"""Elasticsearch service configuration."""

# PostrgreSQL
POSTGRESQL = {
    "POSTGRESQL_VERSION": "POSTGRESQL_9_LATEST",
    "POSTGRESQL_USER": "invenio",
    "POSTGRESQL_PASSWORD": "invenio",
    "POSTGRESQL_DB": "invenio",
}
"""Postgresql service configuration."""

# MySQL
MYSQL = {
    "MYSQL_VERSION": "MYSQL_5_LATEST",
    "MYSQL_USER": "invenio",
    "MYSQL_PASSWORD": "invenio",
    "MYSQL_DB": "invenio",
    "MYSQL_ROOT_PASSWORD": "invenio",
}
"""MySQL service configuration."""

SERVICES = [
    ELASTICSEARCH,
    POSTGRESQL,
    MYSQL,
]
"""List of services to configure."""
