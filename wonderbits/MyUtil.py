from .WBError import wonderbitsError
import re
from .public import DEVICE_TYPE

modules_name_list = DEVICE_TYPE.keys()


class MyUtil(object):
    '''
    wonderbits util set
    '''
    # decide if show console
    is_show_console = False
    _buffer = '###wb-log: '

    _is_serial_error = False
    _serial_error_content = ''

    @staticmethod
    def wb_log(*params):
        '''
            接受不定个数的参数, 并print出来
            '''
        if not MyUtil.is_show_console:
            return
        for param in params:
            MyUtil._buffer = MyUtil._buffer + str(param)
            if MyUtil._buffer.endswith('>'):
                print(MyUtil._buffer, flush=True)
                MyUtil._buffer = '###wb-log: '
            elif MyUtil._buffer.endswith('}'):
                print(MyUtil._buffer, end="", flush=True)
                MyUtil._buffer = '###wb-log: '
            elif MyUtil._buffer.endswith('\n'):
                print(MyUtil._buffer, end="", flush=True)
                MyUtil._buffer = '###wb-log: '

    @staticmethod
    def wb_error_log(*params):
        '''
            接受不定个数的参数, 并print出来
            '''

        print('*' * 50)
        print('###wb-error-log: ')
        for param in params:
            print(param, end="")
        print()
        print('*' * 50)

    @staticmethod
    def wb_decode(raw_byte=b''):
        return raw_byte.decode('gbk')

    @staticmethod
    def wb_encode(raw_str=''):
        return raw_str.encode('utf-8')

    @staticmethod
    def set_serial_error(*params):
        MyUtil._is_serial_error = True
        for err in params:
            if type(err) is str:
                MyUtil._serial_error_content += err
            else:
                MyUtil._serial_error_content += repr(err)
            MyUtil._serial_error_content += '\n'

    @staticmethod
    def serial_error_clear():
        MyUtil._is_serial_error = False
        MyUtil._serial_error_content = ''

    @staticmethod
    def serial_error_check():
        if MyUtil._is_serial_error:
            raise wonderbitsError(MyUtil._serial_error_content[:-1])

    @staticmethod
    def parse_data_from_raw_repl(buffer):
        OK = 'OK'
        beginIndex = buffer.find(OK) + len(OK)
        endIndex = buffer.rfind('\r\n')
        # set_command finished successfully
        if endIndex == -1:
            return 'done'
        # set_command failed
        # get_command finished successfully
        # get_command failed
        return buffer[beginIndex:endIndex]

    @staticmethod
    def mp_error_parse(error_info):
        # print(error_info.encode('gbk'))
        try:
            err_parse_list = error_info.split('\r\n')
            # print(err_parse_list[-1])
            re_obj = re.compile("'(.+)([0-9]+)'")
            # print(re_obj)
            result = re_obj.search(err_parse_list[-1])
            # print(result.group())
            # print(result.group(1))
            # print(result.group(2))
            err_ret = result.group(1)
            # print(err_ret)
            if err_ret in modules_name_list:
                err_ret = err_ret[0].upper() + err_ret[1:] + '({})'.format(
                    result.group(2))
                return "{} isn't defined".format(err_ret)
            else:
                return error_info
        except Exception as e:
            # print('-----------------------except-----------------------')
            # print(e)
            return error_info
