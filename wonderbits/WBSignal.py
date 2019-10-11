from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Signal(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'signal{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def set_rgb(self, r, g, b):
        """
        设置LED灯颜色（r,g,b参数都设置为0时，关闭LED）

        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        
        args = []
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'signal{}.set_rgb({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_buzzer(self, frequency):
        """
        设置蜂鸣器声音频率（Hz）设置频率为0表示关闭蜂鸣器

        :param frequency: 频率：0~20000 Hz
        """

        
        args = []
        args.append(str(frequency))
        command = 'signal{}.set_buzzer({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_vibration(self, strength):
        """
        设置震动马达的震动强度值越大表示震动幅度越大，设置为0时停止震动

        :param strength: 振动幅度：0~100
        """

        
        args = []
        args.append(str(strength))
        command = 'signal{}.set_vibration({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def play_a_note(self, frequency, time, block = None):
        """
        控制蜂鸣器发出一个音调，并持续一段时间

        :param frequency: 频率：20~20000 Hz
        :param time: 时间: 0.05~60 s
        :param block: 阻塞参数：  False: 不阻塞 True: 阻塞 默认为True
        """

        
        args = []
        args.append(str(frequency))
        args.append(str(time))
        if block != None:
            args.append(str(block))
        command = 'signal{}.play_a_note({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    

    