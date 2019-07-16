from .WBits import WBits

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Distance(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    
    def register_distance(self, cb):
        self._register_event('distance{}'.format(self.index), 'distance', cb)
    
    def get_distance(self):
        """
        获取检测的距离值（cm）
        :rtype: float
        """

        command = 'distance{}.get_distance()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        