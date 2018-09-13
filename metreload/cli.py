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
import inspect
import datetime

from metreload.merra2 import get_merra2_data
from metreload.gis import get_shapefile_bbox


def print_usage():
    click.echo("\nExample usage:\n merra2 --collection=M2T1NXFLX --username=<to_be_defined> --password=<to_be_defined> --start_time=\"1980-01-01\"" \
               " --end_time=\"1980-01-02\" --variables=\"['tlml', 'ulml', 'vlml']\" --location=\"[60.2, 24.5,60.1, 24.7]\"")
    click.echo("\nNote that latitude(lat), longitude(lon) is specified as follows:\n location=[<lat-north>,<lon-west>] or" \
               "\n location=[<lat-north>,<lon-west>,<lat-south>,<lon-east>] or" \
               "\n location=\"<path-to-shape-file>\"\n")
       
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
@click.option('-U', '--username', default=getuser(), show_default=True)
@click.option('--password', default=" ")
@click.option('-o', '--output_dir', help="Output directory", default=os.path.curdir, metavar='PATH', show_default=True)
@click.option('--start_time', default="1980-01-01")
@click.option('--end_time', default="1980-01-02")
@click.option('--variables', default= "['tlml', 'ulml', 'vlml']")
@click.option('--location', default= "[60.2, 24.5,60.1, 24.7]")


def merra2(collection, username, password, output_dir, start_time, end_time, variables, location):       
    #Check input arguments    
    click.echo("Download MERRA-2 data\n")
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)    
    errmsg=""
    str_call="Executing command:\nmerra2 "
    for i in args:   
        if str(i)=="password":
            str_call=str_call+"--"+"" +str(i)+"=\"<not_shown>\" "
        else:
            str_call=str_call+"--"+"" +str(i)+"=\""+ str(values[i]) +"\" "
        if values[i] is None or values[i] is "":            
            errmsg="ERROR: Option "+str(i)+"=\""+str(values[i])+"\" is invalid\n"+"Option list: "+str(args)
            click.echo(errmsg)
            print_usage()
            raise click.ClickException("Abort, search log for keyword ERROR")            
    click.echo(str_call+"\n")
    
    #Parse dates
    for option_name, date_text in enumerate(([start_time, end_time])):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            errmsg="ERROR: Option "+str(option_name)+"=\""+str(date_text)+"\" is invalid, should be YYYY-MM-DD"
            click.echo(errmsg)
            print_usage()
            raise click.ClickException("Abort, search log for keyword ERROR")
    
    #Parse variables
    try:
        variables= ast.literal_eval(variables)
    except (ValueError, SyntaxError):
        errmsg="ERROR: Option variables=\""+str(variables)+"\" is invalid."
        click.echo(errmsg)
        print_usage()
        raise click.ClickException("Abort, search log for keyword ERROR")    
    if type(variables) is not list:
        errmsg="ERROR: Option variables=\""+str(variables)+"\" is invalid. Hint: Square bracket notation [] required."
        click.echo(errmsg)            
        print_usage()    
        raise click.ClickException("Abort, search log for keyword ERROR")
    elif not (all(isinstance(n, str) for n in variables)):
        errmsg="ERROR: Option variables=\""+str(variables)+"\" is invalid. Hint: String notation required ['element1','element2'] required."
        click.echo(errmsg)            
        print_usage()   
        raise click.ClickException("Abort, search log for keyword ERROR")

    #Parse location
    if os.path.isfile(location):
        location = get_shapefile_bbox(location)
        #click.echo("Extents are {}".format(extents))  #TODO: Do something meaningful
    else:
        try:
            location= ast.literal_eval(location)
        except (ValueError, SyntaxError):
            errmsg="ERROR: Option location=\""+str(location)+"\" is invalid."
            click.echo(errmsg)            
            print_usage()
            raise click.ClickException("Abort, search log for keyword ERROR")   
        if type(location) is not list:
            errmsg="ERROR: Option location=\""+str(location)+"\" is invalid. Hint: Square bracket notation [] required."
            click.echo(errmsg)            
            print_usage()
            raise click.ClickException("Abort, search log for keyword ERROR")           
    if len(location)==2 or len(location)==4:
        location=tuple(location)
    else:
        errmsg="ERROR: Option location contains an invalid number of arguments "+str(location)
        click.echo(errmsg)
        print_usage()
        raise click.ClickException("Abort, search log for keyword ERROR")
    
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
