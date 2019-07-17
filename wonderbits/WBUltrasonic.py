from .WBits import WBits

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Ultrasonic(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    
    def register_distance(self, cb):
        self._register_event('ultrasonic{}'.format(self.index), 'distance', cb)
    
    def get_distance(self):
        """
        获取超声波检测的距离值（cm）
        :rtype: float
        """

        command = 'ultrasonic{}.get_distance()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        