from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Voice(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'voice{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def speak(self, text, block = None):
        """
        模块正在朗读时若收到新的朗读指令会打断当前朗读内容，然后朗读新内容

        :param text: 朗读内容，可以是字符串，整数，小数
        :param block: 阻塞参数：  False: 不阻塞 True: 阻塞
        """

        text = _format_str_type(text)
        
        args = []
        args.append(str(text))
        if block != None:
            args.append(str(block))
        command = 'voice{}.speak({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def add_command(self, command):
        """
        添加语音识别命令，命令需要使用拼音字符串表示

        :param command: 识别命令，只可以是拼音字符串
        """

        command = _format_str_type(command)
        
        args = []
        args.append(str(command))
        command = 'voice{}.add_command({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_result(self):
        """
        
        :rtype: str
        """

        command = 'voice{}.get_result()'.format(self.index)
        value = self._get_command(command)
        return value
        
    def set_volume(self, val):
        """
        

        :param val: 音量值：0~100
        """

        
        args = []
        args.append(str(val))
        command = 'voice{}.set_volume({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def clear_result(self):
        """
        

        """

        command = 'voice{}.clear_result()'.format(self.index)
        self._set_command(command)

    
    def is_playing(self):
        """
        True：正在朗读False：空闲
        :rtype: bool
        """

        command = 'voice{}.is_playing()'.format(self.index)
        value = self._get_command(command)
        return eval(value)
        

    
    @property
    def source_command(self):
        return self, 'command', []
    
    @property
    def source_play_state(self):
        return self, 'play_state', []
    

    def when_recognized(self, command):
        trigger = 'x=={}'.format(repr(command))
        return Event(self.source_command, trigger)


    