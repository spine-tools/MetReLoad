# -*- coding: utf-8 -*-

"""Console script for reload."""
import sys
import logging

import logzero
import click

from . import __version__
from .merra2 import get_merra2_data


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, default=False, help="Show version and exit")
@click.option('--debug', is_flag=True, default=False)
def cli(version, debug):
    """Console script for metreload."""
    if version:
        click.echo("Version {}".format(__version__))
        return 0
    
    if debug:
        click.echo("Debug mode ON", color='red')
        logzero.loglevel(logging.DEBUG)

    return 0


@cli.command()
@click.option('-c', '--collection', help="Name of MERRA-2 collection (nine-character ESDT code)")
@click.option('-U', '--user', help="Username")
@click.option('--password', prompt=True, hide_input=True)
@click.option('-o', '--output-dir', help="Output directory")              
def merra2(collection, user, password, output_dir):
    click.echo("Downloading MERRA-2 data. . .")
    get_merra2_data(collection, user, password, output_dir)
    click.echo("Done!")


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
