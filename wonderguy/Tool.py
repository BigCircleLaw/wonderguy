
from .WBUpload import WBUpload
from .MyUtil import MyUtil

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