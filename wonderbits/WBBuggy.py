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

    
    def run(self, left, right):
        """
        设置左右两个电机的转动速度

        :param left: 转速：-100~100  符号表示转动方向，绝对值为转动速度
        :param right: 转速：-100~100  符号表示转动方向，绝对值为转动速度
        """

        
        args = []    
        args.append(str(left))
        args.append(str(right))
        command = 'buggy{}.run({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def stop(self):
        """
        左右两个电机停止转动

        """

        command = 'buggy{}.stop()'.format(self.index)
        self._set_command(command)

    
    def set_led1(self, r, g, b):
        """
        设置led1灯颜色（r,g,b参数都设置为0时，关闭LED）

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
        设置led2灯颜色（r,g,b参数都设置为0时，关闭LED）

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

    
    def set_buzzer(self, frequency):
        """
        设置蜂鸣器声音频率（Hz）设置频率为0表示关闭蜂鸣器

        :param frequency: 频率：0~20000 Hz
        """

        
        args = []    
        args.append(str(frequency))
        command = 'buggy{}.set_buzzer({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_distance(self):
        """
        获取检测的距离值（cm）
        :rtype: float
        """

        command = 'buggy{}.get_distance()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def is_line_detected(self, t = None):
        """
        判断某个循迹传感器是否检测为黑
        :rtype: bool
        """

        
        args = []    
        if t != None:
            args.append(str(t))
        command = 'buggy{}.is_line_detected({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value) 
        
    def get_light_s1(self):
        """
        获取s1检测的亮度值，亮度值代表相对强度，值越大代表亮度越强
        :rtype: float
        """

        command = 'buggy{}.get_light_s1()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def get_light_s2(self):
        """
        获取s2检测的亮度值，亮度值代表相对强度，值越大代表亮度越强
        :rtype: float
        """

        command = 'buggy{}.get_light_s2()'.format(self.index)
        value = self._get_command(command)
        return eval(value) 
        
    def set_servo(self, angle):
        """
        设置舵机转动到指定角度使用此函数后舵机将拥有维持角度的扭矩，施加外力改变舵机的角度会很困难

        :param angle: 角度：0~180
        """

        
        args = []    
        args.append(str(angle))
        command = 'buggy{}.set_servo({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def calibrate_with_black(self):
        """
        校准循迹传感器的黑色值

        """

        command = 'buggy{}.calibrate_with_black()'.format(self.index)
        self._set_command(command)

    
    def calibrate_with_white(self):
        """
        

        """

        command = 'buggy{}.calibrate_with_white()'.format(self.index)
        self._set_command(command)

    
    def get_battery_value(self):
        """
        
        :rtype: int
        """

        command = 'buggy{}.get_battery_value()'.format(self.index)
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
        
    def set_calibration_percentage(self, value):
        """
        阈值=循迹传感器检测的黑色值*value%+循迹传感器检测的白色值*（1-value%）

        :param value: 值：0~100
        """

        
        args = []    
        args.append(str(value))
        command = 'buggy{}.set_calibration_percentage({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
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
        

    