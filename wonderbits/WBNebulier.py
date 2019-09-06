from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Nebulier(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'nebulier{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def trun_on(self):
        """
        开启雾化器

        """

        command = 'nebulier{}.trun_on()'.format(self.index)
        self._set_command(command)

    
    def trun_off(self):
        """
        关闭雾化器

        """

        command = 'nebulier{}.trun_off()'.format(self.index)
        self._set_command(command)

    

    

    