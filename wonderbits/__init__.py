from .core import *

import click

from .MyCore import MyCore


@click.group()
@click.option(
    "--port",
    "-p",
    envvar="AMPY_PORT",
    required=False,
    type=click.STRING,
    help=
    "Name of serial port for connected board.  Can optionally specify with AMPY_PORT environment variable.",
    metavar="PORT",
)
def cli(port):
    MyCore.designation_serial_port = port


@cli.command()
@click.argument('file', required=True)  #, help='put file to board')
def upload(file):
    wb_tool.upload.upload(file)


@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    print(local, remote)
    wb_tool.upload.put(local, remote)


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


# del MyCore

if __name__ == "__main__":
    cli()
