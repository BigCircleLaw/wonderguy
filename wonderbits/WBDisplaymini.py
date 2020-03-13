from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Displaymini(WBits):
    BUTTON_NONE = 0x00
    BUTTON_L = 0x01
    BUTTON_R = 0x02
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'displaymini{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def print(self, row, column, text):
        """
        在某个位置显示内容

        :param row: 显示行数：1~16
        :param column: 显示列数：1~15
        :param text: 显示内容，可以是字符串，整数，小数
        """

        text = _format_str_type(text)
        
        args = []
        args.append(str(row))
        args.append(str(column))
        args.append(str(text))
        command = 'displaymini{}.print({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def clear_page(self, page = None):
        """
        清除某页显示的内容

        :param page: 清除的页码：1~8  默认第1页
        """

        
        args = []
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.clear_page({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_chart(self, x, y, page = None):
        """
        以上次传入的坐标为起点，本次坐标为终点画线段。如果是首次使用，则只画单个点

        :param x: X轴坐标：1~119
        :param y: Y轴坐标：1~32
        :param page: 显示页数：1~8  默认画点在第1页
        """

        
        args = []
        args.append(str(x))
        args.append(str(y))
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.draw_chart({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_direction(self, dir = None):
        """
        True:设置显示方向为系统默认显示方向False:设置显示方向为翻转显示方向，使用该函数后显示内容将会进行180°翻转

        :param dir: 方向参数：  False: 设置显示方向为翻转显示方向，使用该函数后显示内容将会进行180°翻转 True: 设置显示方向为系统默认显示方向
        """

        
        args = []
        if dir != None:
            args.append(str(dir))
        command = 'displaymini{}.set_direction({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def turn_to_page(self, page = None):
        """
        转到某页

        :param page: 页码：1~8
        """

        
        args = []
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.turn_to_page({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_button_state(self):
        """
        翻页按钮状态BUTTON_NONE：没有按键按下，值为0BUTTON_L：左键按下，值为1BUTTON_R：右键按下，值为2
        :rtype: int
        """

        command = 'displaymini{}.get_button_state()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def set_page_turning(self, state = None):
        """
        True:开启翻页按键功能False:禁止翻页按键功能禁止翻页按键功能后将不能通过翻页按键来切换不同页码的显示内容系统默认开启翻页按键功能

        :param state: 使能按键参数：  False: 禁止翻页按键功能 True: 开启翻页按键功能
        """

        
        args = []
        if state != None:
            args.append(str(state))
        command = 'displaymini{}.set_page_turning({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_scrollbar(self, state = None):
        """
        True:显示页码滚动指示条False:隐藏页码滚动指示条（屏幕右边的白色小点，用于指示当前页码）系统默认显示页码滚动指示条隐藏后每行最大显示字符数由15变为16

        :param state: 控制参数：  False: 隐藏页码滚动指示条 True: 显示页码滚动指示条
        """

        
        args = []
        if state != None:
            args.append(str(state))
        command = 'displaymini{}.set_scrollbar({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def clear_all_pages(self, block = None):
        """
        清除全部8页显示的内容

        :param block: 阻塞参数：  False: 不阻塞 True: 阻塞
        """

        
        args = []
        if block != None:
            args.append(str(block))
        command = 'displaymini{}.clear_all_pages({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_dot(self, x, y, page = None):
        """
        在画点的页使用print函数会导致已经画过的点消失切换到不同的页码在回到画点的页码也会导致已经画过的点消失

        :param x: X轴坐标：1~119
        :param y: Y轴坐标：1~32
        :param page: 显示页数：1~8  默认第1页
        """

        
        args = []
        args.append(str(x))
        args.append(str(y))
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.draw_dot({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_line(self, head_x, head_y, tail_x, tail_y, page = None):
        """
        在画线的页使用print函数会导致已经画过的线消失切换到不同的页码在回到画线的页码也会导致已经画过的线消失

        :param head_x: 起始点X轴坐标：1~119
        :param head_y: 起始点Y轴坐标：1~32
        :param tail_x: 终止点X轴坐标：1~119
        :param tail_y: 终止点Y轴坐标：1~32
        :param page: 显示页数：1~8  默认第1页
        """

        
        args = []
        args.append(str(head_x))
        args.append(str(head_y))
        args.append(str(tail_x))
        args.append(str(tail_y))
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.draw_line({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def disable_auto_refresh(self):
        """
        禁止自动刷新后，只能调用刷新函数refresh()才能改变显示内容系统默认开启自动刷新显示功能

        """

        command = 'displaymini{}.disable_auto_refresh()'.format(self.index)
        self._set_command(command)

    
    def enable_auto_refresh(self):
        """
        系统默认开启自动刷新显示功能

        """

        command = 'displaymini{}.enable_auto_refresh()'.format(self.index)
        self._set_command(command)

    
    def refresh(self):
        """
        在禁止自动刷新显示功能后只能靠此函数来更新显示内容系统默认开启自动刷新显示功能

        """

        command = 'displaymini{}.refresh()'.format(self.index)
        self._set_command(command)

    
    def draw_save_dot(self, x, y, page = None):
        """
        画点后始终存在，可以使用清屏擦除可与print在同一页显示，显示位置冲突时以画点内容为主

        :param x: X轴坐标：1~119
        :param y: Y轴坐标：1~32
        :param page: 显示页数：1~8  默认第1页
        """

        
        args = []
        args.append(str(x))
        args.append(str(y))
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.draw_save_dot({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_save_line(self, head_x, head_y, tail_x, tail_y, page = None):
        """
        画线后始终存在，可以使用清屏擦除可与print在同一页显示，显示位置冲突时以画线内容为主

        :param head_x: 起始点X轴坐标：1~119
        :param head_y: 起始点Y轴坐标：1~32
        :param tail_x: 终止点X轴坐标：1~119
        :param tail_y: 终止点Y轴坐标：1~32
        :param page: 显示页数：1~8  默认第1页
        """

        
        args = []
        args.append(str(head_x))
        args.append(str(head_y))
        args.append(str(tail_x))
        args.append(str(tail_y))
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.draw_save_line({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_save_chart(self, x, y, page = None):
        """
        以上次传入的坐标为起点，本次坐标为终点画线段。如果是首次使用，则只画单个点

        :param x: X轴坐标：1~119
        :param y: Y轴坐标：1~32
        :param page: 显示页数：1~8  默认画点在第1页
        """

        
        args = []
        args.append(str(x))
        args.append(str(y))
        if page != None:
            args.append(str(page))
        command = 'displaymini{}.draw_save_chart({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def print_big_font(self, row, column, text):
        """
        在某个位置显示大字体内容

        :param row: 显示行数：1~8
        :param column: 显示列数：1~7
        :param text: 显示内容，可以是字符串，整数，小数
        """

        text = _format_str_type(text)
        
        args = []
        args.append(str(row))
        args.append(str(column))
        args.append(str(text))
        command = 'displaymini{}.print_big_font({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    

    