import serial
import serial.tools.list_ports
import os
from .MyUtil import MyUtil as util
import shutil

class WBUpload(object):

    def put(self, file_path):
        '''
        param:file_path:: receive absolute or relative file path
        '''
        if not self._is_empty(file_path):
            try:
                port_list = list(serial.tools.list_ports.comports())
                for i in range(len(port_list)):
                    port = port_list[i]
                    valid_port_flag = False
                    if port.pid == 29987 or port.pid == 60000:
                        valid_port_flag = True
                        currentDir = os.getcwd()
                        source_file_path = file_path
                        if os.path.exists(source_file_path):
                            source_file_path = os.path.join(currentDir, source_file_path)
                        run_loop_path = os.path.join(currentDir, 'run_loop.py')
                        target_file_path = shutil.copy(source_file_path, run_loop_path)
                        util.wb_log(file_path, source_file_path, target_file_path)
                        print('正在下载 {} ...'.format(source_file_path))
                        os.system('ampy -d 2 -p {}  put {}'.format(port.device, target_file_path))
                        os.remove(target_file_path)
                        ser = serial.Serial(port.device, 115200, timeout=1)
                        # reset pyboard manully in windows, because windows system do not reset automatically in first connection.
                        ser.write(b'\x04')
                        print('下载结束')
                        break
                if not valid_port_flag:
                    util.wb_error_log('未发现可用串口！')
            except OSError as e:
                util.wb_error_log(e)
            except Exception as e:
                util.wb_error_log(e)
    
    
    def _is_empty(self, arg):
        is_empty = False
        if not arg:
            is_empty = True
            print('参数不可以为空!')
        return is_empty