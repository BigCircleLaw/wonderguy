from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class IoExtension(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'ioExtension{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def write(self, port, value):
        """
        设置port口输出value%的电压，100%为5V

        :param port: 端口：3~5  只有3~5端口可以输出电压
        :param value: 电压百分比：0~100
        """

        
        args = []
        args.append(str(port))
        args.append(str(value))
        command = 'ioExtension{}.write({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def read(self, port):
        """
        可以读取1~5端口的电压值其中1,2端口的电压为百分比参数，100%表示5v3,4,5端口只能区分0v和5v，True表示5V，False表示0v
        :rtype: float
        """

        
        args = []
        args.append(str(port))
        command = 'ioExtension{}.read({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return self.val_process(value)
        

    

    