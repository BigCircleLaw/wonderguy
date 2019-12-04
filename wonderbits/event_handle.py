import json
# from .event import Event

_event_info = list()


def parse_value(str_val):
    if 'True' == str_val:
        return True
    elif 'False' == str_val:
        return False
    elif '.' in str_val:
        return float(str_val)
    else:
        return int(str_val)


def parse_buffer(json_str):
    d = json.loads(json_str)
    # print(d)
    if 'valuetype' in d:
        if d['valuetype'] == 'list':
            str_list = d['value'].split(',')
            val = list()
            for v in str_list:
                val.append(parse_value(v))
        elif d['valuetype'] == 'string':
            val = d['value']
        elif d['valuetype'] == 'bool':
            val = ((d['value'] == 'True') or (d['value'] == 'true'))
        else:
            val = parse_value(d['value'])
    else:
        val = parse_value(d['value'])
    _event_info[d['target']]._set_originalValue(val)


# def _return_event_start(modulue_name,
#                         source_name,
#                         valueType,
#                         originalValueNum=None):
#     global _event_info
#     if modulue_name not in _event_info:
#         _event_info[modulue_name] = dict()
#     if source_name not in _event_info[modulue_name]:
#         #     _event_info[modulue_name][source_name] = list()
#         # e = Event(valueType, originalValueNum)
#         # _event_info[modulue_name][source_name].append(e)
#         # return e
#         _event_info[modulue_name][source_name] = Event(valueType,
#                                                        originalValueNum)
#     return _event_info[modulue_name][source_name]


def _add_event(event):
    index = len(_event_info)
    _event_info.append(event)
    return index
