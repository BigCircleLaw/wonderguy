from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class LightBelt(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'lightBelt{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def set_leds_rgb(self, start, end, r, g, b):
        """
        设置一段LED灯颜色（r,g,b参数都设置为0时，关闭LED）

        :param start: 起始位置：1~100
        :param end: 结束位置：1~100
        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        
        args = []
        args.append(str(start))
        args.append(str(end))
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'lightBelt{}.set_leds_rgb({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_single_led_rgb(self, num, r, g, b):
        """
        设置单个LED灯颜色（r,g,b参数都设置为0时，关闭LED）

        :param num: 灯的位置：1~100
        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        
        args = []
        args.append(str(num))
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'lightBelt{}.set_single_led_rgb({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def start_rolling(self, start, end, speed):
        """
        滚动区间的起点start可以大于区间终点end滚动方向是start–>end当start大于end时也遵循此规则

        :param start: 滚动区间起点：1~100
        :param end: 滚动区间终点：1~100
        :param speed: 滚动速度：1~100
        """

        
        args = []
        args.append(str(start))
        args.append(str(end))
        args.append(str(speed))
        command = 'lightBelt{}.start_rolling({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def stop_rolling(self):
        """
        

        """

        command = 'lightBelt{}.stop_rolling()'.format(self.index)
        self._set_command(command)

    

    

    