from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Pressure(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'pressure{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_pressure(self):
        """
        获取压力(kg)，量程是0~10KG，超过量程范围可能会导致传感器不修复的损坏
        :rtype: float
        """

        command = 'pressure{}.get_pressure()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def calibrate(self, block = None):
        """
        校准压力感器注意：校准过程中请确保没有外力作用于传感器，否则会导致校准后不准确。校准时，模块指示灯会变为黄色，等待指示灯变蓝说明校准完成了。

        :param block: 阻塞参数  False: 不阻塞 True: 阻塞
        """

        
        args = []
        if block != None:
            args.append(str(block))
        command = 'pressure{}.calibrate({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    
    @property
    def source_pressure(self):
        return self, 'pressure', []
    

    def when_pressure_changed(self, val = 0.2):
        return Event(self.source_pressure, Event.TRIGGER_CHANGED, p)


    