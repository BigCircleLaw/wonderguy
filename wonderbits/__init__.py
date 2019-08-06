from .core import *

import click

# from wonderbits import wb_tool


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', required=True)  #, help='put file to board')
def put(file):
    wb_tool.upload.put(file)


@cli.command()
@click.argument('file', required=True)  #, help='get file content')
def get(file):
    wb_tool.upload.direct_command('get {}'.format(file))


@cli.command()
@click.argument('file', required=True)  #, help='delete file')
def rm(file):
    wb_tool.upload.direct_command('rm {}'.format(file))


@cli.command()
@click.argument('version', required=False)
def update(version):
    if version == None:
        wb_tool.upload.update_bin()
    else:
        wb_tool.upload.update_bin(version)


@cli.command()
def ls():  # list files
    wb_tool.upload.direct_command('ls')


if __name__ == "__main__":
    cli()
