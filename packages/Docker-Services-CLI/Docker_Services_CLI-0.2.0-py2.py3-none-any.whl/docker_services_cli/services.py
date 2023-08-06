# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services module."""

import subprocess
import time

import click

from .config import DOCKER_SERVICES_FILEPATH, MYSQL, POSTGRESQL


def _run_healthcheck_command(command):
    """Runs a given command, returns True if it succeeds, False otherwise."""
    try:
        subprocess.check_call(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def es_healthcheck(*args, **kwargs):
    """Elasticsearch healthcheck."""
    return _run_healthcheck_command([
        "curl",
        "-f",
        "localhost:9200/_cluster/health?wait_for_status=green"
    ])


def postgresql_healthcheck(*args, **kwargs):
    """Postgresql healthcheck."""
    filepath = kwargs['filepath']

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "postgresql",
        "bash",
        "-c",
        "pg_isready",
    ])


def mysql_healthcheck(*args, **kwargs):
    """Mysql healthcheck."""
    filepath = kwargs['filepath']
    password = MYSQL["MYSQL_ROOT_PASSWORD"]

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "mysql",
        "bash",
        "-c",
        f"mysql -p{password} -e \"select Version();\"",
    ])


def redis_healthcheck(*args, **kwargs):
    """Redis healthcheck."""
    filepath = kwargs['filepath']

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "redis",
        "bash",
        "-c",
        "redis-cli ping",
        "|",
        "grep 'PONG'",
        "&>/dev/null;",
    ])


HEALTHCHECKS = {
    "es": es_healthcheck,
    "postgresql": postgresql_healthcheck,
    "mysql": mysql_healthcheck,
    "redis": redis_healthcheck,
}
"""Health check functions module path, as string."""


def wait_for_services(services, filepath=DOCKER_SERVICES_FILEPATH, max_retries=6):
    """Wait for services to be up.

    It performs configured healthchecks in a serial fashion, following the
    order given in the ``up`` command. If the services is an empty list, to be
    compliant with `docker-compose` it will perform the healthchecks of all the
    services.
    """
    if len(services) == 0:
        services = HEALTHCHECKS.keys()

    for service in services:
        exp_backoff_time = 2
        try_ = 1
        # Using plain __import__ to avoid depending on invenio-base
        check = HEALTHCHECKS[service]
        ready = check(filepath=filepath)
        while not ready and try_ < max_retries:
            click.secho(
                f"{service} not ready at {try_} retries, waiting " \
                f"{exp_backoff_time}s",
                fg="yellow"
            )
            try_ += 1
            time.sleep(exp_backoff_time)
            exp_backoff_time *= 2
            ready = check(filepath=filepath)

        if not ready:
            click.secho(f"Unable to boot up {service}", fg="red")
            exit(1)
        else:
            click.secho(f"{service} up and running!", fg="green")


def services_up(services, filepath=DOCKER_SERVICES_FILEPATH, wait=True):
    """Start the given services up.

    docker-compose is smart about not rebuilding an image if
    there is no need to, so --build is not a slow default. In addition
    ``--detach`` is not supported in 1.17.0 or previous.
    """
    command = ["docker-compose", "--file", filepath, "up", "-d"]
    command.extend(services)

    subprocess.check_call(command)
    if wait:
        wait_for_services(services, filepath)


def services_down(filepath=DOCKER_SERVICES_FILEPATH):
    """Stops the given services.

    It does not requries the services. It stops containers and removes
    containers, networks, volumes, and images created by ``up``.
    """
    command = ["docker-compose", "--file", filepath, "down"]

    subprocess.check_call(command)
