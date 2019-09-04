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
        return eval(value) 
        
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

    
    def when_magnet_detected(self, val = None):
        """
        当检测到磁铁时，执行被修饰的函数

        :param val: 磁感强度大于val被认为检测到磁铁，才会触发事件。范围：0~10
        """

        
        args = []    
        if val != None:
            args.append(str(val))
        command = 'hall{}.when_magnet_detected({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    @property
    def source_magnetic(self):
        return self, 'magnetic'
    