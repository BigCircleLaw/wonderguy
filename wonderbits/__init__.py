from .core import *

import click

from .MyCore import MyCore


@click.group(invoke_without_command=True)
# @click.argument('file', required=False)
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
@click.pass_context
# def cli(ctx, file, port):
def cli(ctx, port):
    # print(ctx.invoked_subcommand)
    MyCore.designation_serial_port = port
    if ctx.invoked_subcommand is None:
        # if not file is None:
        #     wb_tool.upload.upload(file)
        # else:
        from .__version__ import VERSION
        print(__version__.VERSION)


@cli.command()
@click.argument('file', required=True)
def upload(file):
    """ put file to board as main.py

    """
    wb_tool.upload.upload(file)


@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    """Put a file or folder and its contents on the board.

    """
    print(local, remote)
    wb_tool.upload.put(local, remote)


@cli.command()
@click.argument("remote_file")
@click.argument("local_file", required=False)
def get(remote_file, local_file):
    """Retrieve a file from the board.

    """
    if local_file == None:
        wb_tool.upload.direct_command('get {}'.format(remote_file))
    else:
        wb_tool.upload.direct_command('get {} {}'.format(
            remote_file, local_file))


@cli.command()
@click.argument('file', required=True)
def rm(file):
    """Remove a file from the board.

    """
    wb_tool.upload.direct_command('rm {}'.format(file))


@cli.command()
@click.argument('version', required=False)
def upgrade(version):
    """Write a binary blob to flash
    
    """
    if version == None:
        wb_tool.upload.update_bin()
    else:
        wb_tool.upload.update_bin(version)


@cli.command()
def ls():
    """List contents of a directory on the board.

    """
    wb_tool.upload.direct_command('ls')


# del MyCore

if __name__ == "__main__":
    cli()
