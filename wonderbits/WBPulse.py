from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Pulse(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'pulse{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_heart_rate(self):
        """
        获取心率（每分钟心脏跳动次数）测量时，从正面（有字的那面）将手指轻轻的贴在绿灯上，等待10秒左右方可测得准确的心率值
        :rtype: int
        """

        command = 'pulse{}.get_heart_rate()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_value(self):
        """
        通过传感器采集的类似心电图的波形，并不是真正的心电图如果没有未读的数据,则返回上一次的值
        :rtype: int
        """

        command = 'pulse{}.get_value()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_value_count(self):
        """
        获取心电波形队列中未读内容的个数（最多存储10个未读内容）返回为0时，说明没有未读取的内容
        :rtype: int
        """

        command = 'pulse{}.get_value_count()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_heart_rate(self):
        return self, 'heart_rate', []
    
    @property
    def source_values(self):
        return self, 'values', []
    

    def when_values_received(self):
        return Event(self.source_values, Event.TRIGGER_UPDATE, None)


    