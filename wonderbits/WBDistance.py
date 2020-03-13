from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Distance(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'distance{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_distance(self):
        """
        获取检测的距离值（cm）
        :rtype: float
        """

        command = 'distance{}.get_distance()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_distance(self):
        return self, 'distance', []
    

    def when_something_detected(self, dis = 30):
        trigger = 'x<' + str(dis)
        return Event(self.source_distance, trigger, dis)


    