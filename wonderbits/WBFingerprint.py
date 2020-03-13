from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Fingerprint(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'fingerprint{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def enroll(self, id = None):
        """
        录入指纹时需要填写编号，执行检测指纹函数时返回对应编号同一个编号被重复录入指纹时，保存最新录入的指纹信息录入指纹过程需要采集同一个指纹三次，每一次采集成功圆圈指示灯亮绿灯，采集失败亮红灯，连续三次采集成功才可录入指纹调用该函数后不能被其他程序打断，只能等待指纹采集成功或者复位

        :param id: 录入指纹的编号
        """

        
        args = []
        if id != None:
            args.append(str(id))
        command = 'fingerprint{}.enroll({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_verified_id(self):
        """
        在检测到指纹前一直返回0，当检测到指纹会返回检测到的指纹编号
        :rtype: int
        """

        command = 'fingerprint{}.get_verified_id()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def is_touched(self):
        """
        传感器被触摸返回True，否则返回False
        :rtype: bool
        """

        command = 'fingerprint{}.is_touched()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_user_num(self):
        """
        
        :rtype: int
        """

        command = 'fingerprint{}.get_user_num()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def delete(self, id = None):
        """
        无参数为删除全部指纹

        :param id: 删除指纹的编号，可不填
        """

        
        args = []
        if id != None:
            args.append(str(id))
        command = 'fingerprint{}.delete({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    
    @property
    def source_touch(self):
        return self, 'touch', []
    
    @property
    def source_verified_id(self):
        return self, 'verified_id', []
    

    def when_user_verified(self, id = 1):
        trigger = 'x==' + str(id)
        return Event(self.source_verified_id, trigger, id)

    def when_touched(self):
        return Event(self.source_touch, Event.TRIGGER_FALSE_TO_TRUE)


    def when_verification_finished(self):
        return Event(self.source_verified_id, Event.TRIGGER_FALSE_TO_TRUE)


    