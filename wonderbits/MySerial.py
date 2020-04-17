'''
@Author: bigcircle
@Date: 2020-03-26 10:30:13
@LastEditTime: 2020-04-16 15:39:19
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \wonderbits-py\wonderbits\MySerial.py
'''
import serial
import serial.tools.list_ports
from .MyUtil import MyUtil
from .WBError import wonderbitsError
import time


def high_bit_1_count(n):
    c = 0
    while (n & 0x80) != 0:
        c += 1
        n <<= 1
    return c


class MySerial(object):
    designation_serial_port = None

    # _ser = None

    def __init__(self):
        self.rec_str = b''
        self._ser = None
        # if not self._ser:
        #     self._connect_serial()
        self._connect_serial()

    def write(self, s):
        try:
            send_content = s.encode('utf-8')
        except AttributeError as err:
            send_content = s
        self._ser.write(send_content)

    def read_handle(self):
        ret = b''
        n = self._ser.inWaiting()
        if n > 0:
            self.rec_str += self._ser.read(n)
            if high_bit_1_count(self.rec_str[-1]) == 0:
                ret = self.rec_str
                self.rec_str = b''
            else:
                position = -1
                count = 1
                while True:
                    if high_bit_1_count(self.rec_str[position]) == 1:
                        count += 1
                        position -= 1
                    elif high_bit_1_count(self.rec_str[position]) == count:
                        ret = self.rec_str
                        self.rec_str = b''
                        break
                    else:
                        ret = self.rec_str[:position]
                        self.rec_str = self.rec_str[position:]
                        break
        return ret.decode('utf-8')

    def read(self):
        # n = self._ser.inWaiting()
        # if n > 0:
        #     rec_str = self._ser.read(n)
        #     return rec_str.decode('utf-8')
        # return ''
        rec_str = self.read_handle()
        return rec_str

    def read_and_compare(self, compare_s, timeout=10, is_exit=True):
        '''
        @description: 读取串口数据直到检测到参数才返回内容，有阻塞效果
                      加入复位处理
        @param str
        @return: 所有收到的内容
        '''
        start_time = time.time()
        try:
            compare_s = compare_s.decode('utf-8')
        except AttributeError as err:
            compare_s = compare_s
        b_buf = ''
        temp_buf = b''
        # compare_len = len(compare_s)
        # reset_len = len(b'Type "help()" for more information.')
        while True:
            temp_buf = self.read_handle()
            for rec_byte in temp_buf:
                # rec_byte = self._ser.read(1)
                b_buf += rec_byte
                if b_buf.endswith(compare_s):
                    return b_buf
                if b_buf.endswith('Type "help()" for more information.'):
                    MyUtil.wb_log('wonderPi reset\n')
                    MySerial._serial_error_exit('MySerial.read_and_compare',
                                                '主控复位，程序停止')
            if time.time() - start_time > timeout:
                if is_exit:
                    # MyUtil.wb_log('MySerial.read_and_compare, timeout')
                    MySerial._serial_error_exit('MySerial.read_and_compare',
                                                '等待超时')
                else:
                    return b_buf

    def state(self):
        if self._ser is None:
            return False
        return self._ser.isOpen()

    def close(self):
        if self._ser:
            self._ser.close()
            del self._ser
            self._ser = None

    def _connect_serial(self):
        '''
            connect serial
            '''
        self.portx = MySerial.choose_serial()
        bps = 115200
        timex = 1
        self._ser = serial.Serial(self.portx, bps, timeout=timex)

    @staticmethod
    def set_serial_port(port):
        '''
        @description: 
        @param {type} 
        @return: 
        '''
        MySerial.designation_serial_port = port

    @staticmethod
    def choose_serial():
        '''
        @description: 
        @param {type} 
        @return: 
        '''
        if MySerial.designation_serial_port == None:
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
                MySerial._serial_error_exit("MySerial.choose_serial",
                                            '未发现可用串口！')
            return portx
        return MySerial.designation_serial_port

    @staticmethod
    def _serial_error_exit(log_output, *err_params):
        '''
        @description: 
        @param {type} 
        @return: 
        '''
        MyUtil.wb_log(log_output, '\r\n')
        err_str = ' '.join(err_params)
        raise wonderbitsError(err_str)
