import os
import serial
from .MyUtil import MyUtil
from .MySerial import MySerial
import shutil
import urllib.request
import time
from .WBError import wonderbitsError


class WBUpload(object):
    def direct_command(self, command, info=None):
        '''
        direct append to last of the wb_ampy
        '''
        port = MySerial.choose_serial()
        if not info is None:
            print(info)
        if port != None:
            os.system('wb_ampy -d 2 -p {} {}'.format(port, command))

    def upload(self, file_path):
        '''
        param:file_path:: receive absolute or relative file path
        '''
        if not self._is_empty(file_path):
            try:
                port = MySerial.choose_serial()
                if port != None:
                    currentDir = os.getcwd()
                    source_file_path = file_path

                    print('正在下载 {} ...'.format(source_file_path))
                    # print('wb_ampy -d 2 -p {}  put {} main.py'.format(
                    #     port, source_file_path))
                    os.system('wb_ampy -d 2 -p {}  put {} main.py'.format(
                        port, source_file_path))
                    # print('_____________________________________')

                    print('下载结束')
                try:
                    if port != None:
                        ser = MySerial()
                        # reset pyboard manully in windows, because windows system do not reset automatically in first connection.
                        ser.write(b'\x04')
                        MyUtil.wb_log(
                            '@rec@ ',
                            ser.read_and_compare('wb init end.\r\n', 5, False))
                        print('开始运行，按Ctrl+C结束')
                        # print('_______________________________________')
                        while True:
                            buffer = ser.read()
                            print(buffer, end='')
                            time.sleep(0.01)
                except KeyboardInterrupt as err:
                    for i in range(3):
                        ser.write(b'\x03')
                    print('运行结束')

                except Exception as e:
                    raise wonderbitsError('读出输出失败:{}'.format(e))
                finally:
                    ser.close()

            except wonderbitsError as e:
                raise e
            # except OSError as e:
            #     raise wonderbitsError('下载失败:{}'.format(e))
            #     # print('下载失败', e)
            except Exception as e:
                raise wonderbitsError('下载失败:{}'.format(e))
                # print('下载失败', e)

    def put(self, source_file_path, designation_file_path):
        if not self._is_empty(source_file_path):
            try:
                port = MySerial.choose_serial()
                if port != None:
                    currentDir = os.getcwd()
                    # source_file_path = file_path
                    if os.path.exists(source_file_path):
                        source_file_path = os.path.join(
                            currentDir, source_file_path)
                    if designation_file_path == None:
                        print('正在下载 {} ...'.format(source_file_path))
                        os.system('wb_ampy -d 2 -p {}  put {}'.format(
                            port, source_file_path))
                    else:
                        print('正在下载 {} to {}...'.format(
                            source_file_path, designation_file_path))
                        os.system('wb_ampy -d 2 -p {}  put {} {}'.format(
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

    def update_bin(self, folder, version=''):
        '''
        param:version:: 
        '''
        try:
            if folder is None:
                des_bin_file = version
            else:
                print('开始更新固件。。。')
                download_url = 'http://wonderbits.cn:3939/board/{}?version={}'.format(
                    folder, version)
                des_bin_file = './wb.bin'
                MyUtil.wb_log(download_url, '\n')
                urllib.request.urlretrieve(download_url, des_bin_file)
                pass

            # print(download_url)
            print('上传固件。。。')
            port = MySerial.choose_serial()
            if port != None:
                # os.system('esptool.py --port ' + port + ' erase_flash')
                os.system('esptool.py --chip esp32 --port ' + port +
                          ' write_flash -z 0x1000 ' + des_bin_file)

            print('更新固件结束！')
            os.system('wb_ampy -d 2 -p {} version'.format(port))
            if not folder is None:
                os.remove(des_bin_file)

        except Exception as error:
            print('更新固件出错：', error)

    def version_ls(self, folder):
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

        MyUtil.wb_log('http://wonderbits.cn:3939/versions/' + folder, '\n')
        with urllib.request.urlopen('http://wonderbits.cn:3939/versions/' +
                                    folder) as f:
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
