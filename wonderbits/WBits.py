from .MyCore import MyCore, wb_core
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

    def __init__(self):
        pass

    def _set_command(self, command):
        '''
        note: send command
        param: command
        return: return 'done' if send command successfully, else return error_msg
        '''
        _lock.acquire()
        try:
            wb_core.write_command(command)
            self._timeout_get_command()
        finally:
            _lock.release()

    def _get_command(self, command):
        '''
        note get command
        params: command
        return: return value if send command successfully, else return error_msg
        '''
        _lock.acquire()
        try:
            cmd = 'print({})'.format(command)
            wb_core.write_command(cmd)
            self._timeout_get_command()
        finally:
            _lock.release()
        return MyCore.return_value

    @staticmethod
    def _timeout_get_command(timeout=3):
        '''
            max time when execute command,
            if exceed max time, ignore current command.
            '''
        MyCore.return_value = None
        time_interval = 0.001
        count = timeout // time_interval
        MyUtil.wb_log('等待命令执行...\n')
        while count > 0:
            MyUtil.serial_error_check()
            if MyCore.return_value != None:
                MyUtil.wb_log('命令执行完成\n')
                return
            time.sleep(time_interval)
            count = count - 1
        MyUtil.wb_log('命令执行超时退出！！！\n')
        # MyCore.can_send_data = True

    def val_process(self, val_str):
        try:
            return eval(val_str)
        except:
            return val_str
