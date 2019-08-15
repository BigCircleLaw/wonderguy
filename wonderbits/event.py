# from .event_handle import _value_comparison
import threading
import os
import time


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

    _FALSE_TO_TRUE_ACTION = 0x00
    _TRUE_TO_FALSE_ACTION = 0x01
    _CHANGED_ACTION = 0x02
    _UPDATE_ACTION = 0x03

    # MORE_THAN_ACTION = 0x03
    # LESS_THAN_ACTION = 0x04

    def __init__(self, valueType, originalValueNum):
        self.originalValueNum = originalValueNum
        if valueType == Event._LIST_VALUE_TYPE:
            self.originalValue = list()
        else:
            self.originalValue = 0

        # self.recordValue = originalValue
        self.valueType = valueType
        # self.actionType = actionType
        # self.eventList = list()
        # self.eventList.append(eventList[0])
        # self.eventList.append(eventList[1])
        self.actionType = 0xFF

    def _triggerDecide(self, actionType, compareValue, delta):
        if self.valueType == self._BOOL_VALUE_TYPE:
            if actionType == self._FALSE_TO_TRUE_ACTION:
                return ((self.originalValue == True)
                        and (compareValue == False), self.originalValue)
            elif actionType == self._TRUE_TO_FALSE_ACTION:
                return ((self.originalValue == False)
                        and (compareValue == True), self.originalValue)
            elif actionType == self._CHANGED_ACTION:
                return ((self.originalValue != compareValue) != 0,
                        self.originalValue)
        elif self.valueType == self._NUMBER_VALUE_TYPE:
            if actionType == self._CHANGED_ACTION:
                return _value_comparison(self.originalValue, compareValue,
                                         delta)
            elif actionType == self._UPDATE_ACTION:
                if self.updateFlag:
                    self.updateFlag = False
                    return True, self.originalValue
                else:
                    return False, self.originalValue
        elif self.valueType == self._STR_VALUE_TYPE:
            pass
        elif self.valueType == self._LIST_VALUE_TYPE:
            if actionType == self._CHANGED_ACTION:
                return _value_comparison(self.originalValue, compareValue,
                                         delta)
            elif actionType == self._UPDATE_ACTION:
                if self.updateFlag:
                    self.updateFlag = False
                    return True, self.originalValue
                else:
                    return False, self.originalValue

    def _set_originalValue(self, value):
        if self.originalValueNum == None:
            self.originalValue = value
        else:
            self.originalValue = value[self.originalValueNum]
        if self.actionType == self._UPDATE_ACTION:
            self.updateFlag = True

    def _compare(self, actionType, delta, interval):
        if actionType == self._UPDATE_ACTION:
            self.actionType = actionType
            self.updateFlag = False

        def event_add_task(func):
            # print(func)

            def event_task_run():
                try:
                    ownData = self.originalValue
                    while True:
                        bool_value, ownData = self._triggerDecide(
                            actionType, ownData, delta)
                        if bool_value:
                            func()
                        time.sleep(interval)
                except OSError:
                    os._exit(0)

            # _thread.stack_size(_THREAD_STACK_SIZE)
            # _thread.start_new_thread(event_task_run, ())
            threading.Thread(target=event_task_run, daemon=True).start()

        return event_add_task
