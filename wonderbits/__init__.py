from .core import *

import click
from wonderbits import wb_tool

def ls(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    wb_tool.upload.direct_command('ls')
    ctx.exit()

@click.command()
@click.option('--ls', is_flag=True, callback=ls,
              expose_value=False, is_eager=True)
@click.option('--file','-f', help='file path')
@click.option('--get',help='get file')
@click.option('--rm', help='rm file')
def upload(file, get, rm):
    if file:
        wb_tool.upload.put(file)
        click.echo("Hello {}!".format(file))
    elif get:
        wb_tool.upload.direct_command('get {}'.format(get))
        click.echo("Hello {}!".format(get))
    elif rm:
        wb_tool.upload.direct_command('rm {}'.format(rm))
        click.echo("Hello {}!".format(rm))

