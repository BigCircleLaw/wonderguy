import serial
import serial.tools.list_ports
import threading
import os
import sys
import time
from .MyUtil import MyUtil
from .event_handle import parse_buffer
from .WBError import wonderbitsError

import textwrap


class MyCore(object):
    '''
    wonderbits mainly handle serial operation（detech, connect, handle_data...）
    '''

    __start_raw_repl_flag = False
    __delete_run_py_flag = False

    # singleton flag
    __init_flag = False

    # get_command_return_value
    return_value = None

    can_send_data = False

    designation_serial_port = None

    # current_time = None
    def __init_property(self):
        '''
        init MyCore property
        '''
        self._ser = None
        self.portx = None

    def __init__(self):
        self.serial_init()

    def _serial_flag_clear(self):
        MyCore.can_send_data = False
        MyCore.__start_raw_repl_flag = False
        pass

    def serial_init(self):
        if not MyCore.__init_flag:
            MyCore.__init_flag = True
            self._serial_flag_clear()
            MyCore.__delete_run_py_flag = False
            MyUtil.serial_error_clear()
            self.__init_property()
            self._try_connect_serial('_try_connect_serial')

    def _try_connect_serial(self, thread_name):
        '''
        try to connect serial
        '''
        try:
            while True:
                self._init_connect()
                if self._ser == None:
                    self._connect_serial()
                else:
                    return
                time.sleep(.5)
        except OSError as e:
            MyCore._serial_error_exception_exit(thread_name, '连接异常')

    def _init_connect(self):
        '''
        get serial ports info
        '''
        if self._ser != None:
            return
        self.__init_property()
        self.portx = MyCore.choose_serial()

    def _connect_serial(self):
        '''
        connect serial
        '''
        try:
            bps = 115200
            timex = 1
            self._ser = serial.Serial(self.portx, bps, timeout=timex)
            # reset pyboard manully in windows, because windows system do not reset automatically in first connection.
            # self._ser.write(b'\x04')
            # MyCore.current_time = time.time()
            threading.Thread(target=self._communication, daemon=True).start()

        except serial.serialutil.SerialException as e:
            # MyUtil.wb_error_log('串口异常{}'.format(e))
            # self.__init_property()
            MyCore._serial_error_exception_exit('_connect_serial',
                                                '串口异常：{}'.format(e))
        except Exception as e:
            # MyUtil.wb_error_log("通用异常：{}".format(e))
            # self.__init_property()
            MyCore._serial_error_exception_exit('_connect_serial',
                                                '通用异常：{}'.format(e))

    def _start_raw_repl(self):
        '''
        start enter raw repl mode
        '''
        if not MyCore.__start_raw_repl_flag:
            MyUtil.wb_log('开始进入raw repl mode', '\r\n')
            MyCore.__start_raw_repl_flag = True
            first_command_list = [b'\r\x03', b'\x03', b'\x03', b'\r\x01']
            for command in first_command_list:
                self._ser.write(command)
                time.sleep(0.01)

    def _delete_run_py_repl(self):
        '''
        delete main.py
        '''
        if not MyCore.__delete_run_py_flag:
            MyUtil.wb_log('开始删除main.py', '\r\n')
            # note: empty_char must be (lenth=1) empty char;
            delete_run_py_command = """
            try:
                import os
            except ImportError:
                import uos as os
            os.remove('main.py')
            """
            delete_run_py_command = textwrap.dedent(delete_run_py_command)
            delete_run_py_end_command = b'\x04'
            self._ser.write(MyUtil.wb_encode(delete_run_py_command))
            self._ser.write(delete_run_py_end_command)
            MyUtil.wb_log(delete_run_py_command, delete_run_py_end_command)

    def _prepare_communication(self, thread_name):
        '''
        brefore communication
        do enter raw repl
        and delete main.py
        and soft reboot
        '''
        try:
            # assume reboot board successfully in 2 second;
            time.sleep(2)
            buffer = ''
            while True:
                if not MyCore.__start_raw_repl_flag:
                    # first step: enter raw repl mode
                    self._start_raw_repl()
                read_len = self._ser.inWaiting()
                if read_len > 0:
                    bufferByte = self._ser.read(read_len)
                    try:
                        bufferChar = MyUtil.wb_decode(bufferByte)
                    except:
                        MyUtil.wb_log('解析数据失败 {}'.format(oneByte))
                        continue
                    for oneChar in bufferChar:
                        buffer += oneChar
                        # MyUtil.wb_log(oneChar)
                        if buffer[-2:] == '\x04>':
                            MyCore.__delete_run_py_flag = True
                            self._ser.write(b'\x04')
                        if oneChar == '>':
                            if 'raw REPL; CTRL-B to exit\r\n>' == buffer[-27:]:
                                # second step: delete run py
                                if not MyCore.__delete_run_py_flag:
                                    self._delete_run_py_repl()
                                else:
                                    MyUtil.wb_log(
                                        '已成功切换到raw repl mode: 可以正常通信了!',
                                        '\r\n')
                                    MyCore.can_send_data = True
                                    return
                            buffer = ''
                        if buffer.endswith(
                                'Type "help()" for more information.'):
                            MyUtil.wb_log('micropyton reset\n')
                            buffer = ''
                            time.sleep(0.5)
                            self._ser.read()
                            self._serial_flag_clear()
                time.sleep(0.003)
        except OSError as e:
            MyCore._serial_thread_error_collection_exit(thread_name, '连接异常')
        except Exception as e:
            MyCore._serial_thread_error_collection_exit(thread_name, '解析异常')

    def _normal_communication(self, thread_name):
        '''
        handle communication data
        '''
        try:
            byte_buffer = b''
            buffer = ''
            while True:
                read_len = self._ser.inWaiting()
                if read_len > 0:
                    bufferByte = self._ser.read(read_len)
                    for oneByte in bufferByte:
                        try:
                            oneChar = chr(oneByte)
                            if oneChar:
                                buffer += oneChar
                                MyUtil.wb_log(oneChar)
                        except:
                            MyUtil.wb_log('解析数据失败 {}'.format(oneByte), '\n')
                            continue
                        if oneByte > 0:
                            # byte_buffer.append(oneByte)
                            if (buffer.startswith('OK')
                                    or buffer.startswith('>OK')
                                ) and buffer.endswith('\x04>'):
                                # parse get_command_return_value
                                get_command_return_value = MyUtil.parse_data_from_raw_repl(
                                    buffer)
                                # output error msg
                                if not buffer.endswith('\x04\x04>'):
                                    # MyUtil.wb_error_log(
                                    #     get_command_return_value)
                                    MyCore.return_value = 'None'
                                    err_output = MyUtil.mp_error_parse(
                                        get_command_return_value)
                                    MyCore._serial_thread_error_collection_exit(
                                        thread_name, err_output)
                                else:
                                    MyCore.return_value = get_command_return_value
                                buffer = b''
                                buffer = ''
                                MyCore.can_send_data = True
                            if buffer.endswith('}'):
                                _start = buffer.find('{')
                                _end = buffer.find('}')
                                if (_start != -1) and (_end !=
                                                       -1) and (_end > _start):
                                    # print(buffer)
                                    str_buffer = buffer[_start:_end + 1]
                                    # print(str_buffer)
                                    parse_buffer(str_buffer)
                                    _bytes_buf = buffer[:_start] + buffer[
                                        _end + 1:]
                                    buffer = _bytes_buf
                            if buffer.endswith(
                                    'Type "help()" for more information.'):
                                MyUtil.wb_log('micropyton reset\n')
                                buffer = ''
                                time.sleep(0.5)
                                self._ser.read()
                                self._serial_flag_clear()
                                return
                time.sleep(0.003)
        except Exception as e:
            MyCore._serial_thread_error_collection_exit(thread_name, '连接异常')

    def _communication(self):
        while True:
            self._prepare_communication('_prepare_communication_thread')
            self._normal_communication('_normal_communication_thread')

    def write_command(self, command):
        MyUtil.serial_error_check()
        cmd = MyUtil.wb_encode(command) + b'\x04'
        while not MyCore.can_send_data:
            # MyUtil.wb_log('MyCore.write_command\r\n')
            MyUtil.serial_error_check()
            time.sleep(.001)
        if MyCore.can_send_data:
            MyUtil.wb_log(cmd, '\r\n')
            self._ser.write(cmd)
            MyCore.can_send_data = False

    @staticmethod
    def choose_serial():
        if MyCore.designation_serial_port == None:
            portx = None
            can_used_serial_port = list()
            port_list = list(serial.tools.list_ports.comports())
            for i in range(len(port_list)):
                port = port_list[i]
                if (port.pid == 0x7523
                        and port.vid == 0x1A86) or (port.pid == 60000
                                                    and port.vid == 0x10C4):
                    can_used_serial_port.append(port)
                    # print(port.hwid)
                    # print(port.pid, port.vid)
                    MyUtil.wb_log(port.device, ' ', port.vid, ' ', port.pid,
                                  '\r\n')
            if len(can_used_serial_port) > 0:
                portx = can_used_serial_port[0].device
            else:
                MyCore._serial_error_exception_exit("choose_serial",
                                                    '未发现可用串口！')
            return portx
        return MyCore.designation_serial_port

    @staticmethod
    def _serial_thread_error_collection_exit(thread_name, *err_params):
        MyCore.__init_flag = False
        MyUtil.wb_log(thread_name, '\r\n')
        MyUtil.set_serial_error(*err_params)
        sys.exit()

    @staticmethod
    def _serial_error_exception_exit(log_output, *err_params):
        MyUtil.wb_log(log_output, '\r\n')
        err_str = ' '.join(err_params)
        raise wonderbitsError(err_str)


# _wb_serial = MyCore()

# if __name__ == "__main__":

#     wbits = WBits()
#     for i in range(10):
#         wbits._send_command('display1.print(1,1,{})'.format(i))
#         value = wbits._get_command('control1.get_sw4()')
