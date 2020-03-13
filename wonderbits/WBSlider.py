from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Slider(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'slider{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_position(self):
        """
        
        :rtype: float
        """

        command = 'slider{}.get_position()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_position(self):
        return self, 'position', []
    

    def when_position_moved(self, val = 1):
        return Event(self.source_position, Event.TRIGGER_CHANGED, val)


    