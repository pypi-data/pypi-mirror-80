# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI module."""

import sys
from distutils.sysconfig import get_python_lib
from pathlib import Path

import click

from .env import set_env
from .services import services_down, services_up


class ServicesCtx(object):
    """Context class for docker services cli."""

    def __init__(self, filepath):
        """Constructor."""
        self.filepath = filepath


@click.group()
@click.version_option()
@click.option(
    "--filepath",
    "-f",
    required=False,
    default=f"{get_python_lib()}/docker_services_cli/docker-services.yml",
    type=click.Path(exists=True),
    help="Path to a docker compose file with the desired services definition.",
)
@click.pass_context
def cli(ctx, filepath):
    """Initialize CLI context."""
    set_env()
    ctx.obj = ServicesCtx(filepath=filepath)

@cli.command()
@click.argument("services", nargs=-1, required=False)  # -1 incompat with default
@click.option(
    "--no-wait",
    is_flag=True,
    help="Wait for services to be up (use healthchecks).",
)
@click.pass_obj
def up(services_ctx, services, no_wait):
    """Boots up the required services."""
    _services = list(services)

    if not _services:
        click.secho("No service was provided... Exiting", fg="red")
        exit(0)  # Do not fail to allow SQLite

    # NOTE: docker-compose boots up all if none is provided
    if len(_services) == 1 and _services[0].lower() == "all":
        _services = []

    services_up(
        services=_services,
        filepath=services_ctx.filepath,
        wait=(not no_wait)
    )
    click.secho("Services up!", fg="green")


@cli.command()
@click.pass_obj
def down(services_ctx):
    """Boots down the required services."""
    services_down(filepath=services_ctx.filepath)
    click.secho("Services down!", fg="green")
