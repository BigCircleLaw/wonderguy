from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Light(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'light{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_light(self):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: int
        """

        command = 'light{}.get_light()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_light(self):
        return self, 'light', []
    

    