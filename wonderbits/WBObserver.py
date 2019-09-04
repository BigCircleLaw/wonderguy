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
        return eval(value) 
        
    def get_humidity(self):
        """
        获取湿度值(%RH）
        :rtype: int
        """

        command = 'observer{}.get_humidity()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def get_light(self):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: int
        """

        command = 'observer{}.get_light()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def get_volume(self):
        """
        声音强度值代表相对强度，值越大代表声音越响
        :rtype: int
        """

        command = 'observer{}.get_volume()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def when_sound_detected(self, val = None):
        """
        当检测到声音时，执行被修饰的函数

        :param val: 声音强度值大于val才会触发事件。范围：0~50
        """

        
        args = []    
        if val != None:
            args.append(str(val))
        command = 'observer{}.when_sound_detected({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    @property
    def source_temperature(self):
        return self, 'temperature'
    @property
    def source_humidity(self):
        return self, 'humidity'
    @property
    def source_light(self):
        return self, 'light'
    @property
    def source_volume(self):
        return self, 'volume'
    