###############################################################################
# Copyright (C) 2018  The Spine Project Authors
#
# This file is part of MetReload
#
# MetReLoad is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

"""Console script for MetReLoad"""

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


@cli.command('merra2', short_help="Get MERRA-2 data")
@click.option('-c', '--collection', help="Name of MERRA-2 collection (nine-character ESDT code)",
              default=None)
@click.option('-U', '--username', default=getuser(), show_default=True)
@click.option('--password', default=' ')
@click.option('-o', '--output-dir', help="Output directory", 
              default=os.path.curdir, metavar='PATH', show_default=True)
@click.option('-E', '--extents', 'extents_shp', help="Get extents from a shapefile layer",
              type=str, default=None, metavar='PATH')
@click.pass_context
def merra2(ctx, collection, username, password, output_dir, extents_shp):
    if collection is None:
        raise click.UsageError("Missing collection name")
    else:
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
