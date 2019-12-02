from .WBError import wonderbitsError


class MyUtil(object):
    '''
    wonderbits util set
    '''
    # decide if show console
    is_show_console = False
    _buffer = ''

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
        return raw_str.encode('gbk')

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
    def set_serial_error(*params):
        MyUtil._is_serial_error = True
        for err in params:
            MyUtil._serial_error_content += '\n'
            if type(err) is str:
                MyUtil._serial_error_content += err
            else:
                MyUtil._serial_error_content += repr(err)

    @staticmethod
    def serial_error_clear():
        MyUtil._is_serial_error = False
        MyUtil._serial_error_content = ''

    @staticmethod
    def serial_error_check():
        if MyUtil._is_serial_error:
            raise wonderbitsError(MyUtil._serial_error_content)
