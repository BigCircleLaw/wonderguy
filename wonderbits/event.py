# from .event_handle import _value_comparison
import threading
import os
import time
from .event_handle import _add_event
from .WBits import WBits
from .MyUtil import MyUtil


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
        self.valueType = source[2]
        self.trigger_type = trigger_type

        index = _add_event(self)

        self.updateFlag = False

        module_name = source[0].__class__.__name__
        send_info = module_name[0].lower(
        ) + module_name[1:] + '{}._register.'.format(
            source[0].index) + source[1] + '({},{},{},{})'.format(
                index, trigger_type, value, interval)
        MyUtil.wb_log(send_info, '\r\n')
        WBits._wb_serial.write_command(send_info)
        WBits._timeout_get_command()
        # print(send_info)

    def _triggerDecide(self, actionType, compareValue, delta):
        if self.valueType == self._BOOL_VALUE_TYPE:
            if actionType == self.TRIGGER_FALSE_TO_TRUE:
                return ((self.originalValue == True)
                        and (compareValue == False), self.originalValue)
            elif actionType == self.TRIGGER_TRUE_TO_FALSE:
                return ((self.originalValue == False)
                        and (compareValue == True), self.originalValue)
            elif actionType == self.TRIGGER_CHANGED:
                return ((self.originalValue != compareValue) != 0,
                        self.originalValue)
        elif self.valueType == self._NUMBER_VALUE_TYPE:
            if actionType == self.TRIGGER_CHANGED:
                return _value_comparison(self.originalValue, compareValue,
                                         delta)
            elif actionType == self.TRIGGER_UPDATE:
                if self.updateFlag:
                    self.updateFlag = False
                    return True, self.originalValue
                else:
                    return False, self.originalValue
        elif self.valueType == self._STR_VALUE_TYPE:
            pass
        elif self.valueType == self._LIST_VALUE_TYPE:
            if actionType == self.TRIGGER_CHANGED:
                return _value_comparison(self.originalValue, compareValue,
                                         delta)
            elif actionType == self.TRIGGER_UPDATE:
                if self.updateFlag:
                    self.updateFlag = False
                    return True, self.originalValue
                else:
                    return False, self.originalValue

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

    # def _compare(self, actionType, delta, interval):
    #     if actionType == self.TRIGGER_UPDATE:
    #         self.trigger_type = actionType
    #         self.updateFlag = False

    #     def event_add_task(func):
    #         # print(func)

    #         def event_task_run():
    #             try:
    #                 ownData = self.originalValue
    #                 while True:
    #                     bool_value, ownData = self._triggerDecide(
    #                         actionType, ownData, delta)
    #                     if bool_value:
    #                         func()
    #                         time.sleep(interval)
    #                     time.sleep(0.01)
    #             except OSError:
    #                 os._exit(0)

    #         threading.Thread(target=event_task_run, daemon=True).start()

    #     return event_add_task

    # def _creat_event(self, triggerDecide, interval):
    #     def event_add_task(func):
    #         # print(func)

    #         def event_task_run():
    #             try:
    #                 while True:
    #                     bool_value = triggerDecide(self.originalValue)
    #                     if bool_value:
    #                         func()
    #                         time.sleep(interval)
    #                     time.sleep(0.01)
    #             except OSError:
    #                 os._exit(0)

    #         # _thread.stack_size(_THREAD_STACK_SIZE)
    #         # _thread.start_new_thread(event_task_run, ())
    #         threading.Thread(target=event_task_run, daemon=True).start()

    #     return event_add_task
