from .MyCore import MyCore
from .MyUtil import MyUtil
import time
import threading
from .WBError import wonderbitsError

_lock = threading.Lock()


class WBits(object):
    '''
    wonderbits parent class
    '''
    # singleton flag
    __init_flag = False

    _wb_serial = None

    def __init__(self):
        if WBits._wb_serial is None:
            MyUtil.wb_log('wonderbits初始化', '\r\n')
            WBits._wb_serial = MyCore()
        else:
            WBits._wb_serial.serial_init()

    def _set_command(self, command):
        '''
        note: send command
        param: command
        return: return 'done' if send command successfully, else return error_msg
        '''
        _lock.acquire()
        try:
            self._wb_serial.write_command(command)
            self._timeout_get_command()
            MyUtil.wb_log(MyCore.return_value, '\r\n')
        finally:
            _lock.release()

        # return MyCore.return_value

    def _get_command(self, command):
        '''
        note get command
        params: command
        return: return value if send command successfully, else return error_msg
        '''
        _lock.acquire()
        try:
            cmd = 'print({})'.format(command)
            self._wb_serial.write_command(cmd)
            self._timeout_get_command()
            MyUtil.wb_log(MyCore.return_value, '\r\n')
            # _lock.release()
            return MyCore.return_value
        # except wonderbitsError as err:
        #     _lock.release()
        #     raise err
        finally:
            _lock.release()

    @staticmethod
    def _timeout_get_command(timeout=3):
        '''
        max time when execute command,
        if exceed max time, ignore current command.
        '''
        MyCore.return_value = None
        time_interval = 0.001
        count = timeout // time_interval
        while count > 0:
            MyUtil.serial_error_check()
            if MyCore.return_value:
                break
            time.sleep(time_interval)
            count = count - 1
            MyCore.can_send_data = True
