import threading
import time
from .MyUtil import MyUtil
from .MySerial import MySerial
from .event_handle import event_parse_buffer

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

    # current_time = None
    def reset_MyCore(self):
        '''
        init MyCore property
        '''
        MyCore.__init_flag = False
        self.close()

    def __init__(self):
        MyCore.__init_flag = False
        self._ser = None

    def _serial_flag_clear(self):
        '''
            @description: 用在线程中，当发现主控复位时需要清掉的flag
            @param {} 
            @return: None
            '''
        MyCore.can_send_data = False
        MyCore.__start_raw_repl_flag = False
        MyCore.__delete_run_py_flag = False

    def serial_init(self):
        if not MyCore.__init_flag:
            MyUtil.wb_log('wonderbits 串口初始化', '\r\n')
            MyCore.__init_flag = True
            self._serial_flag_clear()
            MyUtil.serial_error_clear()
            # self._ser = None
            self._try_connect_serial('_try_connect_serial')

    def _try_connect_serial(self, thread_name):
        '''
        try to connect serial
        '''
        try:
            while True:
                if self._ser is None:
                    self._ser = MySerial()
                    threading.Thread(
                        target=self._communication, daemon=True).start()
                else:
                    return
        except Exception as err:
            self.reset_MyCore()
            raise err

    def _start_raw_repl(self):
        '''
            start enter raw repl mode
            '''
        if not MyCore.__start_raw_repl_flag:
            MyUtil.wb_log('开始进入raw repl mode', '\r\n')
            MyCore.__start_raw_repl_flag = True

            first_command_list = ['\r\x03', '\x03', '\x03', '\r\x01']
            for command in first_command_list[:3]:
                self._ser.write(command)
                time.sleep(0.01)

            count = 0
            MyUtil.wb_log('抛弃开始\n')
            while (count < 20):
                count += 1
                read_str = self._ser.read()
                if read_str:
                    MyUtil.wb_log('抛弃输出 {}\n'.format(read_str))
                    count = 10
                time.sleep(0.1)
            del count
            MyUtil.wb_log('抛弃结束\n')
            for command in first_command_list[3:]:
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
            MyUtil.wb_log('@send@ ', delete_run_py_command)

    def _prepare_communication(self, thread_name):
        '''
            brefore communication
            do enter raw repl
            and delete main.py
            and soft reboot
            '''
        try:
            # assume reboot board successfully in 2 second;
            # time.sleep(2)
            self._start_raw_repl()
            MyUtil.wb_log(
                '@rec@ ',
                self._ser.read_and_compare('raw REPL; CTRL-B to exit\r\n>'))
            self._delete_run_py_repl()
            MyUtil.wb_log('@rec@ ', self._ser.read_and_compare('\x04>'))
            MyCore.__delete_run_py_flag = True
            MyUtil.wb_log('send soft reset\n')
            self._ser.write('\x04')
            MyUtil.wb_log(
                '@rec@ ',
                self._ser.read_and_compare('raw REPL; CTRL-B to exit\r\n>'))
            MyUtil.wb_log('已成功切换到raw repl mode!', '\r\n')
            MyCore.can_send_data = True

        except OSError as e:
            self._serial_thread_error_collection_exit(thread_name, '连接异常')
        except Exception as e:
            self._serial_thread_error_collection_exit(thread_name, '解析异常')

    def _normal_communication(self, thread_name):
        '''
            handle communication data
            '''
        try:
            buffer = ''
            while True:
                bufferChar = self._ser.read()
                for oneChar in bufferChar:
                    if not buffer:
                        MyUtil.wb_log('@rec@ ')
                    MyUtil.wb_log(oneChar)
                    buffer += oneChar

                    if buffer.endswith('\x04>'):
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
                            self._serial_thread_error_collection_exit(
                                thread_name, err_output)
                        else:
                            MyCore.return_value = get_command_return_value
                        buffer = ''
                        MyCore.can_send_data = True
                    if buffer.endswith('}'):
                        _start = buffer.find('{')
                        _end = buffer.find('}')
                        if (_start != -1) and (_end != -1) and (_end > _start):
                            # print(buffer)
                            str_buffer = buffer[_start:_end + 1]
                            # print(str_buffer)
                            event_parse_buffer(str_buffer)
                            _bytes_buf = buffer[:_start] + buffer[_end + 1:]
                            buffer = _bytes_buf
                    if buffer.endswith('Type "help()" for more information.'):
                        MyUtil.wb_log('wonderPi reset\n')
                        self._serial_thread_error_collection_exit(
                            thread_name, '主控复位，程序停止')

                time.sleep(0.007)
        except Exception as e:
            print(e)
            self._serial_thread_error_collection_exit(thread_name, '连接异常')

    def _communication(self):
        while True:
            self._prepare_communication('_prepare_communication_thread')
            self._normal_communication('_normal_communication_thread')

    def write_command(self, command):
        self.serial_init()
        MyUtil.serial_error_check()
        cmd = command + '\x04'
        while not MyCore.can_send_data:
            # MyUtil.wb_log('MyCore.write_command\r\n')
            MyUtil.serial_error_check()
            time.sleep(.01)
        if MyCore.can_send_data:
            MyUtil.wb_log('@send@ ', cmd, '\r\n')
            self._ser.write(cmd)
            MyCore.can_send_data = False
        MyUtil.wb_log('发送命令成功\n')

    def state(self):
        if self._ser is None:
            return False
        return self._ser.state()

    def close(self):
        if self._ser:
            self._ser.close()
            self._ser = None

    def _serial_thread_error_collection_exit(self, thread_name, *err_params):
        self.reset_MyCore()
        MyUtil.thread_error_collection_exit(thread_name, *err_params)

    @staticmethod
    def put_MyCore_flag():
        print('MyCore.__init_flag = {}'.format(MyCore.__init_flag))
        print('MyCore.can_send_data = {}'.format(MyCore.can_send_data))
        print('MyCore.__start_raw_repl_flag = {}'.format(
            MyCore.__start_raw_repl_flag))
        print('MyCore.__delete_run_py_flag = {}'.format(
            MyCore.__delete_run_py_flag))


# _wb_serial = MyCore()

# if __name__ == "__main__":

#     wbits = WBits()
#     for i in range(10):
#         wbits._send_command('display1.print(1,1,{})'.format(i))
#         value = wbits._get_command('control1.get_sw4()')
wb_core = MyCore()
