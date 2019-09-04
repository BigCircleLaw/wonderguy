from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class LightBelt(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index
    
    def set_onboard_rgb(self, rgb):
        command = 'lightBelt{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def set_leds_rgb(self):
        """
        设置一段LED灯颜色（r,g,b参数都设置为0时，关闭LED）

        """

        command = 'lightBelt{}.set_leds_rgb()'.format(self.index)
        self._set_command(command)

    
    def set_single_led_rgb(self):
        """
        设置单个LED灯颜色（r,g,b参数都设置为0时，关闭LED）

        """

        command = 'lightBelt{}.set_single_led_rgb()'.format(self.index)
        self._set_command(command)

    

    