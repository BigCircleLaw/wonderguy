from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Rtc(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'rtc{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_time_str(self):
        """
        返回包含事件信息的字符串，格式为‘year-mouth-dayhour:min:sec’
        :rtype: str
        """

        command = 'rtc{}.get_time_str()'.format(self.index)
        value = self._get_command(command)
        return value
        
    def set_time(self, time):
        """
        设置模块的时间，传入参数为list，列表内容为[year,mouth,day,hour,min,sec]

        :param time: 
        """

        
        args = []
        args.append(str(time))
        command = 'rtc{}.set_time({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_time_list(self):
        """
        返回包含事件信息的列表，列表内容为[year,mouth,day,hour,min,sec,week]
        :rtype: list
        """

        command = 'rtc{}.get_time_list()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_time(self):
        return self, 'time', []
    

    def when_times_up(self, time):
        trigger = 'x==' + str(time)
        return Event(self.source_time, trigger)

    