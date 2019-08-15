from .MyCore import MyCore
from .MyUtil import MyUtil
from .event_handle import _return_event_start
import time
import os
import threading

_lock = threading.Lock()


class WBits(object):
    '''
    wonderbits parent class
    '''
    # singleton flag
    __init_flag = False

    _wb_serial = None

    def __init__(self):
        if not WBits.__init_flag:
            MyUtil.wb_log('wonderbits初始化', '\r\n')
            WBits.__init_flag = True
            WBits._wb_serial = MyCore()

    def _set_command(self, command):
        '''
        note: send command
        param: command
        return: return 'done' if send command successfully, else return error_msg
        '''
        _lock.acquire()
        self._wb_serial.write_command(command)
        self.__timeout_get_command()
        MyUtil.wb_log(MyCore.return_value, '\r\n')
        _lock.release()
        # return MyCore.return_value

    def _get_command(self, command):
        '''
        note get command
        params: command
        return: return value if send command successfully, else return error_msg
        '''
        _lock.acquire()
        cmd = 'print({})'.format(command)
        self._wb_serial.write_command(cmd)
        self.__timeout_get_command()
        MyUtil.wb_log(MyCore.return_value, '\r\n')
        _lock.release()
        return MyCore.return_value

    def __timeout_get_command(self, timeout=3):
        '''
        max time when execute command,
        if exceed max time, ignore current command.
        '''
        try:
            MyCore.return_value = None
            time_interval = 0.001
            count = timeout // time_interval
            while count > 0:
                if MyCore.return_value:
                    break
                time.sleep(time_interval)
                count = count - 1
                MyCore.can_send_data = True
        except KeyboardInterrupt as e:
            MyUtil.wb_log('exit-wb', e)
            os._exit(0)


def _register_event(module, soucre, valueType, actionType, delta, interval):
    WBits._wb_serial.write_command(module + '.register.' + soucre + '()')
    # MyUtil.wb_log(cb)
    e = _return_event_start(module, soucre, valueType)
    return e._compare(actionType, delta, interval)
