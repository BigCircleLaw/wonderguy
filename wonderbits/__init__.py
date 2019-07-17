from .core import *

import click
from wonderbits import wb_tool

@click.command()
@click.option('--file', default='', help='file path')
def upload(file):
    wb_tool.upload.put(file)
    click.echo("Hello {}!".format(file))