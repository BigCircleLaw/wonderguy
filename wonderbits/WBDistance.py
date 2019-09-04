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

        """

        command = 'distance{}.get_distance()'.format(self.index)
        self._set_command(command)

    

    @property
    def source_distance(self):
        return self, 'distance'
    