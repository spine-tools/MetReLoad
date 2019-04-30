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
from datetime import datetime

import logzero
from logzero import logger
import click

from metreload import __version__ as version
from metreload.merra2 import get_merra2_data
from metreload.gis import get_shapefile_bbox


def print_usage(ctx, hint=True):
    """Print usage instructions for given context"""
    click.echo(ctx.get_usage())
    click.echo("""\nExample usage:\n
               merra2 --collection=M2T1NXFLX --username=<to_be_defined>
               --password=<to_be_defined> --start_time=1980-01-01
               --end_time=1980-01-02 --variables=tlml,ulml,vlml --location=60.2,24.5,60.1,24.7""")
    click.echo("""\nNote that latitude (lat), longitude (lon) is specified as follows:\n
               location=<lat-north>,<lon-west> or\n
               location=<lat-north>,<lon-west>,<lat-south>,<lon-east> or\n
               location=<path-to-shape-file>""")
    if hint:
        click.echo("\nTry `metreload COMMAND --help` for more options")


def print_help(ctx):
    """Print help for given context"""
    click.echo(ctx.get_help())
    print_usage(ctx, hint=False)


@click.group(invoke_without_command=True)
@click.version_option(version)
@click.option('--debug', is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug):
    """MetReLoad: an application for downloading meteorological reanalysis data"""
    if debug:
        click.echo("Debug mode ON")
        logzero.loglevel(logging.DEBUG)
    else:
        logzero.loglevel(logging.INFO)

    if ctx.invoked_subcommand is None:
        print_help(ctx)


@cli.command('merra2', short_help="Get MERRA-2 data")
@click.option('-c', '--collection', help="Name of MERRA-2 collection (nine-character ESDT code)",
              default=None)
@click.option('-U', '--username', default=getuser(), show_default=True)
@click.option('--password', default=" ")
@click.option('-o', '--output-dir', help="Output directory", metavar='PATH',
              default=os.path.curdir, show_default=True)
@click.option('--start-time', help="Start date (YYYY-MM-DD)", metavar='DATE', required=True)
@click.option('--end-time', help="End date (YYYY-MM-DD)", metavar='DATE', required=True)
@click.option('--variables', help="Comma separated list of variable names",
              metavar='LIST', default=None)
@click.option('--location', default=None, metavar='ARG', required=True,
              help="Comma separated list of coordinates either (lat,lon or north,west,south,east) "
                   "or path to shapefile")
@click.pass_context
def merra2(ctx, collection, username, password, output_dir,
           start_time, end_time, variables, location):
    """Command for downloading MERRA-2 data"""
    if collection is None:
        raise click.UsageError("Missing collection name")

    # Parse dates
    for date_text in [start_time, end_time]:
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            errmsg = "Option '{}' is invalid, should be YYYY-MM-DD".format(date_text)
            click.echo(errmsg)
            print_usage(ctx)
            raise click.BadParameter(errmsg)
        except TypeError:
            raise click.UsageError("Start or end time missing")

    # Parse variables
    if variables is not None:
        try:
            variables_list = [x.strip() for x in variables.split(',')]
        except:
            errmsg = "Option 'variables={}' is invalid.".format(variables)
            print_usage(ctx)
            raise click.BadParameter(errmsg, param_hint='variables')
    else:
        variables_list = None

    # Parse location
    if os.path.isfile(location):
        try:
            coords = get_shapefile_bbox(location)
        except RuntimeError:
            raise click.BadParameter("Could not derive location form shapefile",
                                     param_hint='location')
    else:
        try:
            coords = tuple([float(x) for x in location.split(',')])
        except ValueError:
            errmsg = "Option location=\""+str(location)+"\" is invalid."
            print_usage(ctx)
            raise click.BadParameter(errmsg, param_hint='location')
    if len(coords) not in (2, 4):
        errmsg = "Option location contains an invalid number of arguments {}".format(location)
        click.echo(errmsg)
        print_usage(ctx)
        raise click.BadParameter(errmsg, param_hint='location')

    click.echo("Downloading MERRA-2 data . . .")
    try:
        get_merra2_data(collection, username, password, output_dir,
                        start_time, end_time, variables_list, coords)
    except RuntimeError as err:
        logger.error(str(err))
        raise click.ClickException(err)
    else:
        click.echo("Done!")


def main():  # pylint: disable=C0111
    cli(obj={})  # pylint: disable=E1120,E1123


if __name__ == "__main__":
    main()
