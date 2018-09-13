# -*- coding: utf-8 -*-

"""Console script for reload."""
import sys
import os.path
import logging
from getpass import getuser

import logzero
from logzero import logger
import click
import ast

from metreload.merra2 import get_merra2_data


def print_usage():
    click.echo("\nExample usage:\n merra2 --collection=M2T1NXFLX --username=<to_be_defined> --password=<to_be_defined> --start_time=\"1980-01-01\"" \
    "\n        --end_time=\"1980-01-02\" --variables=\"['tlml', 'ulml', 'vlml']\" --location=\"[60.2, 24.5,60.1, 24.7]\"")
    click.echo("Note that latitude(lat), longitude(lon) is specified as follows:\n location=[<lat-north>,<lon-west>] or" \
               "\n location=[<lat-north>,<lon-west>,<lat-south>,<lon-east>] ")
       
def print_help(ctx):    
    click.echo(ctx.get_help())
    print_usage()

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
@click.option('-c', '--collection', help="Name of MERRA-2 collection (nine-character ESDT code)")
@click.option('-U', '--username', default=getuser)
@click.option('--password', default='')
@click.option('-o', '--output-dir', help="Output directory", default=os.path.curdir)
@click.option('--start_time', default='1980-01-01')
@click.option('--end_time', default='1980-01-02')
@click.option('--variables', default= "['tlml', 'ulml', 'vlml']")
@click.option('--location', default= "[60.2, 24.5,60.1, 24.7]")

def merra2(collection, username, password, output_dir, start_time, end_time, variables, location):    
    
    click.echo("Download MERRA-2 data\n")
    
    #Check input arguments
    for (key,value) in locals().items():
        if value is (None or ""):
            print ("ERROR: Option \"",key,"\" holds an invalid value \"", value ,"\"")
            keylist = []
            keylist.extend(iter(locals().keys()))
            keylist = keylist[:-1]              
            print ("Option list: ", keylist)
            print_usage()
            break
            exit() 
            
    click.echo("Downloading started")
    #Parse variables
    try:
        variables= ast.literal_eval(variables)
    except SyntaxError:
        print ("ERROR: Option variables is invalid ", variables)
        print_usage()
        exit()
    #Parse location    
    try:
        location= ast.literal_eval(location)
    except SyntaxError:
        print ("ERROR: Option location is invalid ", location)
        print_usage()
        exit()  
    if len(location)==2:
        lat=location[0]
        lon=location[1]
        assert lat > -90 and lat < 90  # TODO: Better error messages
        assert lon > -180 and lon < 180        
    elif len(location)==4:
        #west, east, south, north = location
        north, west, south, east = location
        assert (west < east and south < north)  # TODO: better error messages
        assert all(lon > -180 and lon < 180 for lon in (west, east))
        assert all(lat > -90 and lat < 90 for lat in (south, north))
    else:
        print ("ERROR: Option location contains an invalid number of arguments ", location)
        print_usage()
        exit()    
    #Call merra2.py    
    try:
        get_merra2_data(collection, username, password, output_dir, start_time, end_time, variables, location)
    except RuntimeError as err:
        logger.error(str(err))
        raise click.ClickException(err)
    else:
        click.echo("Done!")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
