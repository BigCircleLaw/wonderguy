'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-07-26 11:28:22
@LastEditTime: 2019-08-12 14:04:53
@LastEditors: Please set LastEditors
'''
import os
import serial
from .MyUtil import MyUtil as util
from .MyCore import MyCore
import shutil
import urllib.request


class WBUpload(object):
    def direct_command(self, command):
        '''
        direct append to last of the ampy
        '''
        port = MyCore.choose_serial()
        if port != None:
            os.system('ampy -d 2 -p {} {}'.format(port, command))

    def upload(self, file_path):
        '''
        param:file_path:: receive absolute or relative file path
        '''
        if not self._is_empty(file_path):
            try:
                port = MyCore.choose_serial()
                if port != None:
                    currentDir = os.getcwd()
                    source_file_path = file_path
                    if os.path.exists(source_file_path):
                        source_file_path = os.path.join(
                            currentDir, source_file_path)
                    run_loop_path = os.path.join(currentDir, 'main.py')
                    target_file_path = shutil.copy(source_file_path,
                                                   run_loop_path)
                    # util.wb_error_log(file_path, ', ', source_file_path,
                    #                   ', ', target_file_path)
                    print('正在下载 {} ...'.format(source_file_path))
                    os.system('ampy -d 2 -p {}  put {}'.format(
                        port, target_file_path))
                    os.remove(target_file_path)
                    ser = serial.Serial(port, 115200, timeout=1)
                    # reset pyboard manully in windows, because windows system do not reset automatically in first connection.
                    ser.write(b'\x04')
                    print('下载结束')
                    ser.close()

            except OSError as e:
                print('下载失败', e)
            except Exception as e:
                print('下载失败', e)

    def put(self, source_file_path, designation_file_path):
        if not self._is_empty(source_file_path):
            try:
                port = MyCore.choose_serial()
                if port != None:
                    currentDir = os.getcwd()
                    # source_file_path = file_path
                    if os.path.exists(source_file_path):
                        source_file_path = os.path.join(
                            currentDir, source_file_path)
                    if designation_file_path == None:
                        print('正在下载 {} ...'.format(source_file_path))
                        os.system('ampy -d 2 -p {}  put {}'.format(
                            port, source_file_path))
                    else:
                        print('正在下载 {} to {}...'.format(
                            source_file_path, designation_file_path))
                        os.system('ampy -d 2 -p {}  put {} {}'.format(
                            port, source_file_path, designation_file_path))
                    ser = serial.Serial(port, 115200, timeout=1)
                    # reset pyboard manully in windows, because windows system do not reset automatically in first connection.
                    ser.write(b'\x04')
                    print('下载结束')
                    ser.close()

            except OSError as e:
                print('下载失败', e)
            except Exception as e:
                print('下载失败', e)

    def _is_empty(self, arg):
        is_empty = False
        if not arg:
            is_empty = True
            print('参数不可以为空!')
        return is_empty

    def update_bin(self, version=''):
        '''
        param:version:: 
        '''
        try:
            print('开始更新固件。。。')
            download_url = 'http://wonderbits.cn:3939/lib/wonderbits-{}.bin'.format(
                version)
            des_bin_file = './wb.bin'
            urllib.request.urlretrieve(download_url, des_bin_file)
            # print(download_url)
            print('上传固件。。。')
            port = MyCore.choose_serial()
            if port != None:
                # os.system('esptool.py --port ' + port + ' erase_flash')
                os.system('esptool.py --chip esp32 --port ' + port +
                          ' write_flash -z 0x1000 ' + des_bin_file)

            print('更新固件结束！')
        except OSError as error:
            print('更新固件出错：', error)
        except Exception as error:
            print('更新固件出错：', error)

    def version_ls(self):
        def bytes_to_list(bytes_list):
            transform_flag = False
            # record = ''
            version_list = list()
            for val in bytes_list:
                if chr(val) == '"' and transform_flag:
                    transform_flag = False
                    version_list.append(record)
                else:
                    if transform_flag:
                        record += chr(val)

                    if chr(val) == '"' and not transform_flag:
                        transform_flag = True
                        record = ''

            return version_list

        with urllib.request.urlopen('http://wonderbits.cn:3939/versions') as f:
            text = f.read()
            # print(text)
            # print(bytes_to_list(text))
            version_list = bytes_to_list(text)
            if len(version_list) > 0:
                print('以下版本固件可更新：')
                for val in version_list:
                    print(val)
            else:
                print('没有可更新固件版本！！！')
