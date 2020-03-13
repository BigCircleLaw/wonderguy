from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Climate(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'climate{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_temperature(self):
        """
        获取温度值（°C）
        :rtype: int
        """

        command = 'climate{}.get_temperature()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_humidity(self):
        """
        获取湿度值(%RH）
        :rtype: int
        """

        command = 'climate{}.get_humidity()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_temperature(self):
        return self, 'temperature', []
    
    @property
    def source_humidity(self):
        return self, 'humidity', []
    

    