from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Hall(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'hall{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_magnetic(self):
        """
        
        :rtype: float
        """

        command = 'hall{}.get_magnetic()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def calibrate(self, block = None):
        """
        校准霍尔传感器注意：校准过程中请确保没有磁性物体靠近模块，否则会导致校准后不准确。校准时，模块指示灯会变为黄色，等待指示灯变蓝说明校准完成了。

        :param block: 阻塞参数  False: 不阻塞 True: 阻塞
        """

        
        args = []
        if block != None:
            args.append(str(block))
        command = 'hall{}.calibrate({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    
    @property
    def source_magnetic(self):
        return self, 'magnetic', []
    

    def when_magnet_detected(self, val = 2):
        trigger = 'abs(x)>' + str(val)
        return Event(self.source_magnetic, trigger, val)


    