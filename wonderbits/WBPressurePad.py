from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class PressurePad(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'pressurePad{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_pressure(self):
        """
        
        :rtype: float
        """

        command = 'pressurePad{}.get_pressure()'.format(self.index)
        value = self._get_command(command)
        return eval(value)
        

    
    @property
    def source_pressure(self):
        return self, 'pressure', []
    

    def when_pressure(self):
        return Event(self.source_pressure, Event.TRIGGER_FALSE_TO_TRUE, val)

    