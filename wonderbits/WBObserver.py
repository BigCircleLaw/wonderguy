from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Observer(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'observer{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_temperature(self):
        """
        获取温度值（°C）
        :rtype: int
        """

        command = 'observer{}.get_temperature()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_humidity(self):
        """
        获取湿度值(%RH）
        :rtype: int
        """

        command = 'observer{}.get_humidity()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_light(self):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: int
        """

        command = 'observer{}.get_light()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_volume(self):
        """
        声音强度值代表相对强度，值越大代表声音越响
        :rtype: int
        """

        command = 'observer{}.get_volume()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_temperature(self):
        return self, 'temperature', []
    
    @property
    def source_humidity(self):
        return self, 'humidity', []
    
    @property
    def source_light(self):
        return self, 'light', []
    
    @property
    def source_volume(self):
        return self, 'volume', []
    

    def when_sound_detected(self, val = 10):
        trigger = 'x>' + str(val)
        return Event(self.source_volume, trigger, val)


    