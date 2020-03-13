from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Nfc(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'nfc{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def is_card_found(self):
        """
        判断是否在传感器附近检测到卡片
        :rtype: bool
        """

        command = 'nfc{}.is_card_found()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def write(self, zone, msg):
        """
        写入信息到nfc卡的指定区域写入内容纯英文数字内容不超过16个字符，纯汉字内容不超过8个汉字

        :param zone: 清除的页码：1~40  默认第1页
        :param msg: 写入的内容
        """

        msg = _format_str_type(msg)
        
        args = []
        args.append(str(zone))
        args.append(str(msg))
        command = 'nfc{}.write({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def read(self, zone):
        """
        读取nfc卡的指定区域读取内容纯英文数字内容不超过16个字符，纯汉字内容不超过8个汉字
        :rtype: str
        """

        
        args = []
        args.append(str(zone))
        command = 'nfc{}.read({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return value
        

    
    @property
    def source_card_found(self):
        return self, 'card_found', []
    

    def when_card_found(self):
        return Event(self.source_card_found, Event.TRIGGER_FALSE_TO_TRUE)


    