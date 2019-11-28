from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Multimeter(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'multimeter{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_resistance(self):
        """
        
        :rtype: float
        """

        command = 'multimeter{}.get_resistance()'.format(self.index)
        value = self._get_command(command)
        return eval(value)
        
    def get_voltage(self):
        """
        
        :rtype: float
        """

        command = 'multimeter{}.get_voltage()'.format(self.index)
        value = self._get_command(command)
        return eval(value)
        
    def turn_on_display(self):
        """
        系统默认开启显示功能

        """

        command = 'multimeter{}.turn_on_display()'.format(self.index)
        self._set_command(command)

    
    def turn_off_display(self):
        """
        系统默认开启显示功能

        """

        command = 'multimeter{}.turn_off_display()'.format(self.index)
        self._set_command(command)

    

    
    @property
    def source_resistance(self):
        return self, 'resistance', []
    
    @property
    def source_voltage(self):
        return self, 'voltage', []
    

    