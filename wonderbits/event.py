# from .event_handle import _value_comparison
import threading
import time
from .event_handle import _add_event
from .WBits import WBits
from .MyUtil import MyUtil
from .MyCore import wb_core


def _value_comparison(newValue, oldValue, varyValue):
    if type(newValue) != type(oldValue):
        return True, newValue
    elif isinstance(oldValue, list):
        # print(newValue)
        # print(oldValue)
        return newValue != oldValue, newValue.copy()
    else:
        return abs(newValue - oldValue) >= varyValue, oldValue if abs(
            newValue - oldValue) < varyValue else newValue


class Event:

    _BOOL_VALUE_TYPE = 0x00
    _NUMBER_VALUE_TYPE = 0x01
    _STR_VALUE_TYPE = 0x02
    _LIST_VALUE_TYPE = 0x03

    TRIGGER_FALSE_TO_TRUE = 0x00
    TRIGGER_TRUE_TO_FALSE = 0x01
    TRIGGER_CHANGED = 0x02
    TRIGGER_UPDATE = 0x03

    # MORE_THAN_ACTION = 0x03
    # LESS_THAN_ACTION = 0x04

    def __init__(self,
                 source,
                 trigger_type,
                 value=None,
                 interval=None,
                 originalValueNum=None):

        self.originalValueNum = originalValueNum
        self.originalValue = 0

        if type(trigger_type) is str:
            trigger_type = repr(trigger_type)
        index = _add_event(self)

        self.updateFlag = False

        module_name = source[0].__class__.__name__
        send_info = module_name[0].lower(
        ) + module_name[1:] + '{}._register.'.format(
            source[0].index) + source[1] + '('
        send_info += '{},{},{},{}'.format(index, trigger_type, value, interval)
        if source[2]:
            send_info += ',' + ','.join(map(str, source[2]))
        send_info += ')'
        MyUtil.wb_log(send_info, '\r\n')
        wb_core.write_command(send_info)
        WBits._timeout_get_command()
        # print(send_info)

    def __call__(self, func):
        self.updateFlag = False

        def event_task_run():
            while True:
                if self.updateFlag == True:
                    func(self.originalValue)
                    self.updateFlag = False
                time.sleep(0.01)

        threading.Thread(target=event_task_run, daemon=True).start()

    def _set_originalValue(self, value):
        if self.originalValueNum == None:
            self.originalValue = value
        else:
            self.originalValue = value[self.originalValueNum]
        self.updateFlag = True
