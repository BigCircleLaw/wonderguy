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
        return self.val_process(value)
        
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
        return self.val_process(value)
        
    def get_light_s1(self):
        """
        获取s1检测的亮度值，亮度值代表相对强度，值越大代表亮度越强
        :rtype: float
        """

        command = 'buggy{}.get_light_s1()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_light_s2(self):
        """
        获取s2检测的亮度值，亮度值代表相对强度，值越大代表亮度越强
        :rtype: float
        """

        command = 'buggy{}.get_light_s2()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
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
        获取电池电量值
        :rtype: int
        """

        command = 'buggy{}.get_battery_value()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_tracking_status(self):
        """
        
        :rtype: list
        """

        command = 'buggy{}.get_tracking_status()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_tracking_values(self):
        """
        
        :rtype: list
        """

        command = 'buggy{}.get_tracking_values()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def set_tracking_rate(self, value):
        """
        设置循迹传感器的黑白阈值百分比为value阈值=循迹传感器检测的黑色值*value%+循迹传感器检测的白色值*（1-value%）

        :param value: 值：0~100
        """

        
        args = []
        args.append(str(value))
        command = 'buggy{}.set_tracking_rate({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    
    @property
    def source_battery_value(self):
        return self, 'battery_value', []
    
    @property
    def source_s1(self):
        return self, 's1', []
    
    @property
    def source_s2(self):
        return self, 's2', []
    
    @property
    def source_distance(self):
        return self, 'distance', []
    
    @property
    def source_tracer_state(self):
        return self, 'tracer_state', []
    
    @property
    def source_tracer_states(self):
        return self, 'tracer_states', []
    
    @property
    def source_tracer_values(self):
        return self, 'tracer_values', []
    

    def when_blocked(self, dis = 30):
        trigger = 'x<' + str(dis)
        return Event(self.source_distance, trigger, dis)


    def when_line_detected_left(self):
        trigger = 'x<0x04 and x>0x00'
        return Event(self.source_tracer_state, trigger)


    def when_line_detected_right(self):
        trigger = 'x>0x04'
        return Event(self.source_tracer_state, trigger)


    def when_any_black_detected(self):
        trigger = 'x!=[False, False, False, False, False]'
        return Event(self.source_tracer_states, trigger)


    