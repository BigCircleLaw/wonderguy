import click
import os

from ampy import pyboard, files

from .Tool import wb_tool
from .MyCore import MyCore, wb_core
from .MyUtil import MyUtil
from .WBError import wonderbitsError

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True)
# @click.argument('file', required=False)
@click.option(
    "--port",
    "-p",
    required=False,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="PORT",
)
@click.option(
    "--version", "-v", is_flag=True, help="Get version for sdk, firmware")
@click.option("--log", "-L", is_flag=True, help="print log information")
def cli(port, version, log):
    MyCore.designation_serial_port = port

    if wb_core.state():
        wb_core.close()

    try:
        if version:
            from .__version__ import __version__
            print('Python SDK version is', __version__)
            wb_tool.upload.direct_command('version', '正在获取固件版本，请稍后...')
    except wonderbitsError as e:
        print('未连接豌豆拼设备!')
    except Exception as e:
        raise e

    if log:
        wb_tool.show_console()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('file', required=True)
def upload(file):
    """ Put file to board as main.py.

    """
    wb_tool.upload.upload(file)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    """Put a file or folder and its contents on the board.

    Put will upload a local file or folder  to the board.  If the file already
    exists on the board it will be overwritten with no warning!  You must pass
    at least one argument which is the path to the local file/folder to
    upload.  If the item to upload is a folder then it will be copied to the
    board recursively with its entire child structure.  You can pass a second
    optional argument which is the path and name of the file/folder to put to
    on the connected board.

    For example to upload a main.py from the current directory to the board's
    root run:

      wonderbits put main.py

    Or to upload a board_boot.py from a ./foo subdirectory and save it as boot.py
    in the board's root run:

      wonderbits put ./foo/board_boot.py boot.py

    To upload a local folder adafruit_library and all of its child files/folders
    as an item under the board's root run:

      wonderbits put adafruit_library

    Or to put a local folder adafruit_library on the board under the path
    /lib/adafruit_library on the board run:

      wonderbits put adafruit_library /lib/adafruit_library
    """
    # Use the local filename if no remote filename is provided.
    MyUtil.wb_log(local, remote)
    wb_tool.upload.put(local, remote)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("remote_file")
@click.argument("local_file", required=False)
def get(remote_file, local_file):
    """
    Retrieve a file from the board.

    Get will download a file from the board and print its contents or save it
    locally.  You must pass at least one argument which is the path to the file
    to download from the board.  If you don't specify a second argument then
    the file contents will be printed to standard output.  However if you pass
    a file name as the second argument then the contents of the downloaded file
    will be saved to that file (overwriting anything inside it!).

    For example to retrieve the boot.py and print it out run:

      wonderbits get boot.py

    Or to get main.py and save it as main.py locally run:

      wonderbits get main.py main.py
    """
    # Get the file contents.
    if local_file == None:
        wb_tool.upload.direct_command('get {}'.format(remote_file))
    else:
        wb_tool.upload.direct_command('get {} {}'.format(
            remote_file, local_file))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('file', required=True)
def rm(file):
    """Remove a file from the board.

    Remove the specified file from the board's filesystem.  Must specify one
    argument which is the path to the file to delete.  Note that this can't
    delete directories which have files inside them, but can delete empty
    directories.

    For example to delete main.py from the root of a board run:

      wonderbits rm main.py
    """
    # Delete the provided file/directory on the board.
    wb_tool.upload.direct_command('rm {}'.format(file))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--ls', '-l', is_flag=True, help="Get the version allowed to be updated.")
@click.option(
    "--file", "-f", required=False, type=click.STRING, help="下载本地文件。")
@click.argument('version', required=False)
def upgrade(ls, version, file):
    """Write a binary blob to flash.

    """
    if not file is None:
        wb_tool.upload.update_bin(None, file)
    else:
        _board = pyboard.Pyboard(
            MyCore.choose_serial(), baudrate=115200, rawdelay=2)
        board_files = files.Files(_board)
        version_val = board_files.version()
        _board.close()
        if '-' in version_val:
            hardware_str = version_val.split('-')[0]
        else:
            hardware_str = 'wonderbits'
        MyUtil.wb_log(hardware_str, '\n')
        if ls:
            wb_tool.upload.version_ls(hardware_str)
        else:
            if version == None:
                wb_tool.upload.update_bin(hardware_str)
            else:
                wb_tool.upload.update_bin(hardware_str, version)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("directory", default="/")
@click.option(
    "--long_format",
    "-l",
    is_flag=True,
    help=
    "Print long format info including size of files.  Note the size of directories is not supported and will show 0 values.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="recursively list all files and (empty) directories.",
)
def ls(directory, long_format, recursive):
    """List contents of a directory on the board.

    Can pass an optional argument which is the path to the directory.  The
    default is to list the contents of the root, /, path.

    For example to list the contents of the root run:

      wonderbits ls

    Or to list the contents of the /foo/bar directory on the board run:

      wonderbits ls /foo/bar

    Add the -l or --long_format flag to print the size of files (however note
    MicroPython does not calculate the size of folders and will show 0 bytes):

      wonderbits ls -l /foo/bar
    """
    # List each file/directory on a separate line.
    command = 'ls ' + directory

    if long_format:
        command += ' -l'

    if recursive:
        command += ' -r'

    wb_tool.upload.direct_command(command)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('directory', required=False)
def mkdir(directory):
    """
    Create a directory on the board.

    Mkdir will create the specified directory on the board.  One argument is
    required, the full path of the directory to create.

    Note that you cannot recursively create a hierarchy of directories with one
    mkdir command, instead you must create each parent directory with separate
    mkdir command calls.

    For example to make a directory under the root called 'code':

      wonderbits mkdir /code
    """
    # Run the mkdir command.
    wb_tool.upload.direct_command('mkdir {}'.format(directory))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("remote_folder")
def rmdir(remote_folder):
    """Forcefully remove a folder and all its children from the board.

    Remove the specified folder from the board's filesystem.  Must specify one
    argument which is the path to the folder to delete.  This will delete the
    directory and ALL of its children recursively, use with caution!

    For example to delete everything under /adafruit_library from the root of a
    board run:

      wonderbits rmdir adafruit_library
    """
    # Delete the provided file/directory on the board.
    wb_tool.upload.direct_command('rmdir {}'.format(remote_folder))


@cli.command(context_settings=CONTEXT_SETTINGS)
def reset():
    """Perform soft reset/reboot of the board.

    Will connect to the board and perform a reset.  Depending on the board
    and firmware, several different types of reset may be supported.

      wonderbits reset
    """
    wb_tool.upload.direct_command('reset')
