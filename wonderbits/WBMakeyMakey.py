from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class MakeyMakey(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'makeyMakey{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def is_touched(self, pad):
        """
        获取某通道是否被触摸
        :rtype: bool
        """

        
        args = []
        args.append(str(pad))
        command = 'makeyMakey{}.is_touched({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return self.val_process(value)
        

    def source_state(self, pad):
        args = []
        args.append(pad)
        return self, 'state', args
    
    @property
    def source_state_1(self):
        return self, 'state_1', []
    
    @property
    def source_state_2(self):
        return self, 'state_2', []
    
    @property
    def source_state_3(self):
        return self, 'state_3', []
    
    @property
    def source_state_4(self):
        return self, 'state_4', []
    
    @property
    def source_state_5(self):
        return self, 'state_5', []
    
    @property
    def source_state_6(self):
        return self, 'state_6', []
    
    @property
    def source_state_7(self):
        return self, 'state_7', []
    
    @property
    def source_state_8(self):
        return self, 'state_8', []
    
    @property
    def source_state_9(self):
        return self, 'state_9', []
    
    @property
    def source_state_10(self):
        return self, 'state_10', []
    
    @property
    def source_state_11(self):
        return self, 'state_11', []
    
    @property
    def source_state_12(self):
        return self, 'state_12', []
    
    @property
    def source_state_13(self):
        return self, 'state_13', []
    
    @property
    def source_state_14(self):
        return self, 'state_14', []
    
    @property
    def source_state_15(self):
        return self, 'state_15', []
    
    @property
    def source_state_16(self):
        return self, 'state_16', []
    
    @property
    def source_state_17(self):
        return self, 'state_17', []
    
    @property
    def source_state_18(self):
        return self, 'state_18', []
    

    def when_pad_touched(self, pad):
        return Event(self.source_state(pad), Event.TRIGGER_FALSE_TO_TRUE)

    