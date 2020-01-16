from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Transmitter(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'transmitter{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_char(self):
        """
        使用该函数可得到最近一次收到的莫尔斯解码内容
        :rtype: str
        """

        command = 'transmitter{}.get_char()'.format(self.index)
        value = self._get_command(command)
        return value
        
    def set_led(self, state = None):
        """
        False:关闭指示灯True:开启指示灯

        :param state: 参数：  False: 关闭指示灯 True: 开启指示灯
        """

        
        args = []
        if state != None:
            args.append(str(state))
        command = 'transmitter{}.set_led({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_buzzer(self, state = None):
        """
        False:关闭蜂鸣器True:开启指示灯

        :param state: 参数：  False: 关闭蜂鸣器 True: 开启指示灯
        """

        
        args = []
        if state != None:
            args.append(str(state))
        command = 'transmitter{}.set_buzzer({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_speed(self, speed = None):
        """
        调用此函数设置莫尔斯码的速度，速度越快‘.’,’_’按下时间越短

        :param speed: 莫尔斯码速度， 范围 0~100
        """

        
        args = []
        if speed != None:
            args.append(str(speed))
        command = 'transmitter{}.set_speed({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    
    @property
    def source_msg(self):
        return self, 'msg', []
    
    @property
    def source_press_time(self):
        return self, 'press_time', []
    

    def when_msg_decoded(self):
        return Event(self.source_msg, Event.TRIGGER_UPDATE)


    def when_key_released(self):
        return Event(self.source_press_time, Event.TRIGGER_UPDATE)


    