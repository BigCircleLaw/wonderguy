from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class MakeyMakey(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index
    
    def set_onboard_rgb(self, rgb):
        command = 'makeymakey{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def is_touched(self):
        """
        获取某通道是否被触摸

        """

        command = 'makeymakey{}.is_touched()'.format(self.index)
        self._set_command(command)

    
    def source_state(self):
        """
        

        """

        command = 'makeymakey{}.source_state()'.format(self.index)
        self._set_command(command)

    

    