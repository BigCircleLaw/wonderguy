import serial
import serial.tools.list_ports
import threading
import os
import time
from .MyUtil import MyUtil

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

    # current_time = None

    def __init_property(self):
        '''
        init MyCore property
        '''
        self._ser = None
        self._can_used_serial_port = []

    def __init__(self):
        if not MyCore.__init_flag:
            MyCore.__init_flag = True
            self.__init_property()
            threading.Thread(target=self._try_connect_serial_thread, args=('connect_serial_thread',), daemon=True).start()

    def _try_connect_serial_thread(self, thread_name):
        '''
        try to connect serial
        '''
        try:
            while True:
                self._init_connect()
                can_used_serial_count = len(self._can_used_serial_port)
                if not can_used_serial_count:
                    MyUtil.wb_error_log('无可用串口')
                    os._exit(0)
                else:
                    if self._ser == None and can_used_serial_count != 0:
                        self._connect_serial()
                    time.sleep(.5)
        except KeyboardInterrupt as e:
            MyUtil.wb_error_log('退出豌豆拼')
            os._exit(0)
        except OSError as e:
            MyUtil.wb_error_log('连接异常')
            os._exit(0)
        

    def _init_connect(self):
        '''
        get serial ports info
        '''
        if self._ser != None:
            return
        self.__init_property()
        port_list = list(serial.tools.list_ports.comports())
        for i in range(len(port_list)):
            port = port_list[i]
            if port.pid == 29987 or port.pid == 60000:
                self._can_used_serial_port.append(port)
                MyUtil.wb_log(port, port.pid)

    def _connect_serial(self):
        '''
        connect serial
        '''
        try:
            portx = self._can_used_serial_port[0].device
            bps = 115200
            timex = 1
            self._ser = serial.Serial(portx, bps, timeout=timex)
            # reset pyboard manully in windows, because windows system do not reset automatically in first connection.
            # self._ser.write(b'\x04')
            # MyCore.current_time = time.time()
            threading.Thread(target=self._prepare_communication, args=('handle_serial_port_target',), daemon=True).start()
            
            # assume reboot board successfully in 2 second;
            time.sleep(2)
            # first step: enter raw repl mode
            self._start_raw_repl()
        except serial.serialutil.SerialException as e:
            MyUtil.wb_error_log('串口异常{}',format(e))
            self.__init_property()
        except Exception as e:
            MyUtil.wb_error_log("通用异常：{}".format(e))
            self.__init_property()
        

    def _prepare_communication(self, target_name):
        '''
        brefore communication
        do enter raw repl
        and delete run_loop.py
        and soft reboot
        '''
        try:
            buffer = ''
            while True:
                oneByte = self._ser.read(1)
                try:
                    oneChar = MyUtil.wb_decode(oneByte)
                except:
                    MyUtil.wb_log('解析数据失败 {}'.format(oneByte))
                    continue
                if oneChar:
                    buffer += oneChar
                    if oneByte == b'\n':
                        MyUtil.wb_log(buffer)
                        if 'raw REPL; CTRL-B to exit\r\n' == buffer:
                            # second step: delete run py
                            if not MyCore.__delete_run_py_flag:
                                self._delete_run_py_repl()
                            else:
                                MyUtil.wb_log('已成功切换到raw repl mode: 可以正常通信了!', '\r\n')
                                MyCore.can_send_data = True
                                threading.Thread(target=self._normal_communication, args=('normal_communication_thread',), daemon=True).start()
                                break
                        buffer = ''
                    if buffer.startswith('>OK'):
                            # third step(last step): soft reboot enter raw repl
                            self._ser.write(b'\x04')
                            buffer = ''
                    if oneChar == '>' and buffer[-3:] == '>>>':
                        # MyUtil.wb_log(time.time() - MyCore.current_time)
                        MyUtil.wb_log(buffer)
                        buffer = ''
                        # # first step: enter raw repl mode
                        # self._start_raw_repl()
        except OSError as e:
            MyUtil.wb_error_log('连接异常')
            os._exit(0)

    def _start_raw_repl(self):
        '''
        start enter raw repl mode
        '''
        if not MyCore.__start_raw_repl_flag:
            MyUtil.wb_log('开始进入raw repl mode')
            MyCore.__start_raw_repl_flag = True
            first_command_list = [b'\r\x03\x03', b'\r\x01']
            for command in first_command_list:
                self._ser.write(command)
    
    def _delete_run_py_repl(self):
        '''
        delete run_loop.py
        '''
        if not MyCore.__delete_run_py_flag:
            MyUtil.wb_log('开始删除run_loop.py')
            MyCore.__delete_run_py_flag = True
            # note: empty_char must be (leng=1) char;
            empty_char = ' '
            delete_run_py_command = "try:\r\n" + empty_char * 4 + "import os\r\nexcept ImportError:\r\n" + empty_char * 4 + "import uos as os\r\nos.remove('run_loop.py')\r\n"
            delete_run_py_end_command = b'\x04'
            self._ser.write(MyUtil.wb_encode(delete_run_py_command))
            self._ser.write(delete_run_py_end_command)
            MyUtil.wb_log(delete_run_py_command, delete_run_py_end_command)

    def _normal_communication(self, target_name):
        '''
        handle communication data
        '''
        try:
            byte_buffer = b''
            buffer = ''
            while True:
                oneByte = self._ser.read(1)
                try:
                    oneChar = MyUtil.wb_decode(oneByte)
                    if oneChar:
                        buffer += oneChar
                except:
                    MyUtil.wb_log('解析数据失败 {}'.format(oneByte))
                    continue
                if oneByte:
                    byte_buffer += oneByte
                    if (byte_buffer.startswith(b'OK') or byte_buffer.startswith(b'>OK')) and byte_buffer.endswith(b'\x04>'):
                        # parse get_command_return_value
                        get_command_return_value = MyUtil.parse_data_from_raw_repl(buffer)
                        MyCore.return_value = get_command_return_value
                        # output error msg
                        if not byte_buffer.endswith(b'\x04\x04>'):
                            MyUtil.wb_error_log(get_command_return_value)
                        else:
                            MyUtil.wb_log(byte_buffer)
                        byte_buffer = b''
                        buffer = ''
                        MyCore.can_send_data = True
        except OSError as e:
            MyUtil.wb_error_log('连接异常')
            os._exit(0)

    def write_command(self, command):
        try:
            cmd = MyUtil.wb_encode(command) + b'\x04'
            while not MyCore.can_send_data:
                time.sleep(.001)
            if MyCore.can_send_data:
                MyUtil.wb_log(cmd)
                self._ser.write(cmd)
                MyCore.can_send_data = False
        except KeyboardInterrupt as e:
            MyUtil.wb_error_log('exit-wb')
            os._exit(0)



# if __name__ == "__main__":

#     wbits = WBits()
#     for i in range(10):
#         wbits._send_command('display1.print(1,1,{})'.format(i))
#         value = wbits._get_command('control1.get_sw4()')

