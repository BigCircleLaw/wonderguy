import json
from .event import Event

_event_info = dict()


def parse_buffer(json_str):
    d = json.loads(json_str)
    # print(d['type'])
    # print(d['module'])
    # print(d['source'])
    # print(d['value'])
    _event_info[d['module']][d['source']]._set_originalValue(d['value'])


def _return_event_start(modulue_name,
                        source_name,
                        valueType,
                        originalValueNum=0):
    global _event_info
    if modulue_name not in _event_info:
        _event_info[modulue_name] = dict()
    if source_name not in _event_info[modulue_name]:
        #     _event_info[modulue_name][source_name] = list()
        # e = Event(valueType, originalValueNum)
        # _event_info[modulue_name][source_name].append(e)
        # return e
        _event_info[modulue_name][source_name] = Event(valueType,
                                                       originalValueNum)
    return _event_info[modulue_name][source_name]


def _set_event_value(eventNameList, valueList, select=None):
    if select == None:
        for name in eventNameList:
            if name in _event_info:
                _event_info[name]._set_originalValue(valueList)
    else:
        try:
            _event_info[select]._set_originalValue(valueList)
        except:
            pass
