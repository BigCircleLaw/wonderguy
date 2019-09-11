from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class LedMatrix(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'ledMatrix{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def print(self, text):
        """
        显示数字，字符等

        :param text: 显示内容，可以是字符串，整数，小数
        """

        text = _format_str_type(text)
        
        args = []
        args.append(str(text))
        command = 'ledMatrix{}.print({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def clear(self):
        """
        清除已经显示的内容

        """

        command = 'ledMatrix{}.clear()'.format(self.index)
        self._set_command(command)

    
    def set_scrolling(self, state):
        """
        控制点阵模块的显示形式系统默认关闭连续滚动显示

        :param state: 控制参数：  False: 关闭连续滚动显示 True: 开启连续滚动显示
        """

        
        args = []
        args.append(str(state))
        command = 'ledMatrix{}.set_scrolling({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_dot(self, x, y):
        """
        在点阵上画点，使用该函数会使正在滚动的点阵停止滚动如果画点之后，在使用print函数会将画过的内容清除

        :param x: X轴坐标：1~16
        :param y: Y轴坐标：1~8
        """

        
        args = []
        args.append(str(x))
        args.append(str(y))
        command = 'ledMatrix{}.draw_dot({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def draw_line(self, head_x, head_y, tail_x, tail_y):
        """
        在点阵上画线，使用该函数会使正在滚动的点阵停止滚动如果画线之后，在使用print函数会将画过的内容清除

        :param head_x: 起始点X轴坐标：1~16
        :param head_y: 起始点Y轴坐标：1~8
        :param tail_x: 终止点X轴坐标：1~16
        :param tail_y: 终止点Y轴坐标：1~8
        """

        
        args = []
        args.append(str(head_x))
        args.append(str(head_y))
        args.append(str(tail_x))
        args.append(str(tail_y))
        command = 'ledMatrix{}.draw_line({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    

    