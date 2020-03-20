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
    help="连接豌豆派的串口名称。",
    metavar="PORT")
@click.option("--version", "-v", is_flag=True, help="得到SDK版本；连接豌豆派时可以获得固件版本。")
@click.option("--log", "-L", is_flag=True, help="加入这个参数可以得到运行时的log输出。")
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
    """ 
    上传文件作为main.py.

    \b
    FILE是你要选择上传的本地文件，它可以不命名为main.py
    main.py会在豌豆派开机时执行

    使用示例：

      wonderbits upload test.py

    """
    wb_tool.upload.upload(file)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    """
    将文件或文件夹的内容传到豌豆派中.

    \b
    将把本地文件或文件夹上载到板上。如果文件已经存在于开发板上，它将直接被覆盖！
    您需要传递至少一个参数，该参数是要上传的本地文件/文件夹的路径。
    如果要上载的项目是文件夹，则它将以其整个子结构递归复制到板上。
    您可以传递第二个可选参数，该参数是要放在连接的板上的文件/文件夹的路径和名称。


    上传main.py到豌豆派的根目录：

      wonderbits put main.py

    或者从test文件夹中把test_boot.py上传到豌豆拼作为boot.py：

      wonderbits put ./test/test_boot.py boot.py

    上传test文件夹及其子文件到豌豆派的根目录下：

      wonderbits put test

    获奖test文件夹上传到lib/test路径下：

      wonderbits put test /lib/test
    """
    # Use the local filename if no remote filename is provided.
    MyUtil.wb_log(local, remote)
    wb_tool.upload.put(local, remote)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("remote_file")
@click.argument("local_file", required=False)
def get(remote_file, local_file):
    """
    从豌豆派读取一个文件.

    get命令将从豌豆派上读取一个文件内容，将其打印或者保存到本地文件。
    该命令需要至少一个参数，第一个参数是板子上的文件路径，如果没有第二个参数则将会吧内容打印出来。
    如果存在第二个参数，将会作为文件名。豌豆派文件的内容将保存到对应文件中（如果文件已存在则覆盖其中的任何内容！）。

    例如打印boot.py：

      wonderbits get boot.py

    或者读取main.py到本地的main.py

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
    """
    删除豌豆派上的一个文件.

    \b
    从豌豆派上删除一个文件。有且只有一个参数，该参数用于指定将要删除的文件路径。
    注意：这不能删除包含文件的文件夹，但可以删除空文件夹。

    删除根目录下的main.py文件:

      wonderbits rm main.py
    """
    # Delete the provided file/directory on the board.
    wb_tool.upload.direct_command('rm {}'.format(file))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--ls', '-l', is_flag=True, help="获取可更新的固件列表.")
@click.option(
    "--file", "-f", required=False, type=click.STRING, help="下载本地文件。")
@click.argument('version', required=False)
def upgrade(ls, version, file):
    """
    更新豌豆派固件.

    VERSION是用于指定更新固件的版本。
    如果不填写该参数测默认更新最新的固件版本。
    
    更新最新的豌豆派固件：

      wonderbits upgrade
    
    如果想查询可更新的固件列表，可使用--ls或-l：

      wonderbits upgrade -l
    
    需要更新本地文件可以使用--file或-f：

      wonderbits upgrade -f my_firmware.bin

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
    help="打印文件大小。注意：不计算文件夹大小，显示0字节。",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="递归查询所有文件和文件夹。",
)
def ls(directory, long_format, recursive):
    """
    查询豌豆派的文件目录.

    传递一个参数作为查询的文件夹，默认值是根目录文件夹。

    查询根目录:

      wonderbits ls

    查询lib文件夹的文件目录:

      wonderbits ls /lib

    添加--long_format或-l可以打印文件大小（注意：不计算文件夹大小，显示0字节）：

      wonderbits ls -l /liab
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
    在豌豆派上创建一个文件夹.

    创建一个指定文件夹。需要一个参数作为完整的路径。

    /b
    注意：不能递归的创建一个文件夹。
    列如：需要创建/test1/test2，或test1不存在，你只能先创建test1再去创建test2.

    创建一个名为'code'的文件夹:

      wonderbits mkdir /code
    """
    # Run the mkdir command.
    wb_tool.upload.direct_command('mkdir {}'.format(directory))


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("remote_folder")
def rmdir(remote_folder):
    """
    删除豌豆派上的文件夹及其所有子项.

    \b
    从豌豆派的文件系统中产出指定文件夹。需要一个参数作为要删除的文件夹路径。
    注意：使用该命令递归删除所有子项，请谨慎使用。

    删除lib文件夹下所有内容：

      wonderbits rmdir lib
    """
    # Delete the provided file/directory on the board.
    wb_tool.upload.direct_command('rmdir {}'.format(remote_folder))


@cli.command(context_settings=CONTEXT_SETTINGS)
def reset():
    """
    复位豌豆派.

    将连接豌豆派并执行复位。

    复位豌豆派:
    
      wonderbits reset
    """
    wb_tool.upload.direct_command('reset')
