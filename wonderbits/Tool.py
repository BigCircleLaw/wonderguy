from .WBUpload import WBUpload
from .MyUtil import MyUtil
from .MyCore import MyCore


class wb_tool(object):
    '''
    豌豆拼工具集合
    '''
    upload = WBUpload()

    @staticmethod
    def show_console():
        '''
        开启控制台输出
        '''
        MyUtil.is_show_console = True

    @staticmethod
    def hide_console():
        '''
            隐藏控制台输出（默认）
            '''
        MyUtil.is_show_console = False

    @staticmethod
    def put_all_flag():
        '''
            隐藏控制台输出（默认）
            '''
        print('MyUtil.is_show_console = {}'.format(MyUtil.is_show_console))
        MyCore.put_MyCore_flag()
