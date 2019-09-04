from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Buggy(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index
    
    def set_onboard_rgb(self, rgb):
        command = 'buggy{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_battery_value(self):
        """
        
        :rtype: int
        """

        command = 'buggy{}.get_battery_value()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def set_buzzer(self, frequency):
        """
        设置频率为0表示关闭蜂鸣器

        :param frequency: 频率：0~20000 Hz
        """

        
        args = []    
        args.append(str(frequency))
        command = 'buggy{}.set_buzzer({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_led1(self, r, g, b):
        """
        

        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        
        args = []    
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'buggy{}.set_led1({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_led2(self, r, g, b):
        """
        

        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        
        args = []    
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'buggy{}.set_led2({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def set_motors(self, speed_left, speed_right):
        """
        符号表示转动方向，绝对值为转动速度

        :param speed_left: 转速：-100~100  符号表示转动方向，绝对值为转动速度
        :param speed_right: 转速：-100~100  符号表示转动方向，绝对值为转动速度
        """

        
        args = []    
        args.append(str(speed_left))
        args.append(str(speed_right))
        command = 'buggy{}.set_motors({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_s1(self):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: float
        """

        command = 'buggy{}.get_s1()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def get_s2(self):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: float
        """

        command = 'buggy{}.get_s2()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def get_tracer_all_black_state(self):
        """
        True：循迹传感器全部检测为黑False：循迹传感器任意一个检测到白
        :rtype: bool
        """

        command = 'buggy{}.get_tracer_all_black_state()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def get_tracer_all_white_state(self):
        """
        True：循迹传感器全部检测为白False：循迹传感器任意一个检测到黑
        :rtype: bool
        """

        command = 'buggy{}.get_tracer_all_white_state()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def is_tracer_check_black(self, channel):
        """
        表示t1~t5
        :rtype: bool
        """

        
        args = []    
        args.append(str(channel))
        command = 'buggy{}.is_tracer_check_black({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value) 
        
    def get_tracer_value(self, channel):
        """
        表示t1~τ5
        :rtype: float
        """

        
        args = []    
        args.append(str(channel))
        command = 'buggy{}.get_tracer_value({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value) 
        
    def is_t6_check_unobstructed(self):
        """
        True：t6无遮挡False：t6被遮挡
        :rtype: bool
        """

        command = 'buggy{}.is_t6_check_unobstructed()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def is_t7_check_unobstructed(self):
        """
        True：t7无遮挡False：t7被遮挡
        :rtype: bool
        """

        command = 'buggy{}.is_t7_check_unobstructed()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def set_calibration_percentage(self, value):
        """
        阈值=循迹传感器检测的黑色值*value%+循迹传感器检测的白色值*（1-value%）

        :param value: 值：0~100
        """

        
        args = []    
        args.append(str(value))
        command = 'buggy{}.set_calibration_percentage({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def calibration_black(self):
        """
        

        """

        command = 'buggy{}.calibration_black()'.format(self.index)
        self._set_command(command)

    
    def calibration_white(self):
        """
        

        """

        command = 'buggy{}.calibration_white()'.format(self.index)
        self._set_command(command)

    

    