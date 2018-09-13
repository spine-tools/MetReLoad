# -*- coding: utf-8 -*-

"""Console script for reload."""
import sys
import os.path
import logging
from getpass import getuser

import logzero
from logzero import logger
import click

from metreload.merra2 import get_merra2_data
from metreload.gis import get_shapefile_bbox


def print_help(ctx):
    click.echo(ctx.get_help())


@click.group(invoke_without_command=True)
@click.version_option()
@click.option('--debug', is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug):
    """MetReLoad: an application for downloading meteorological reanalysis data"""
    if debug:
        click.echo("Debug mode ON")
        logzero.loglevel(logging.DEBUG)

    if ctx.invoked_subcommand is None:
        print_help(ctx)


@cli.command()
@click.option('-c', '--collection', help="Name of MERRA-2 collection (nine-character ESDT code)",
              required=True)
@click.option('-U', '--username', default=getuser(), show_default=True)
@click.option('--password', default=' ')
@click.option('-o', '--output-dir', help="Output directory", 
              default=os.path.curdir, metavar='PATH', show_default=True)
@click.option('-E', '--extents', 'extents_shp', help="Get extents from a shapefile layer",
              type=str, default=None, metavar='PATH')
def merra2(collection, username, password, output_dir, extents_shp):
    click.echo("Downloading MERRA-2 data . . .")
    if extents_shp is not None:
        extents = get_shapefile_bbox(extents_shp)
        click.echo("Extents are {}".format(extents))  #TODO: Do something meaningful
    try:
        get_merra2_data(collection, username, password, output_dir)
    except RuntimeError as err:
        logger.error(str(err))
        raise click.ClickException(err)
    else:
        click.echo("Done!")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
