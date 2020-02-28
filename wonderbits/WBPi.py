from .WBits import WBits
from .event import Event


def _format_str_type(x):
    if isinstance(x, str):
        x = str(x).replace('"', '\\"')
        x = "\"" + x + "\""
    return x


class Pi(WBits):
    def __init__(self, index=1):
        WBits.__init__(self)
        self.index = ''

    def set_onboard_rgb(self, rgb):
        command = 'Pi{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    def print(self, row, column, *text):
        """
        在某个位置显示内容，位置坐标以像素点为单位

        :param row: 显示行数：1~64
        :param column: 显示列数：1~128
        :param text: 显示内容，可以是字符串，整数，小数
        """

        args = []
        args.append(str(row))
        args.append(str(column))
        for i in text:
            i = _format_str_type(i)
            args.append(str(i))
        command = 'Pi{}.print({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def draw_chart(self, x, y=None):
        """
        以上次传入的坐标为起点，本次坐标为终点画线段。如果是首次使用，则只画单个点

        :param x: X轴坐标：1~128
        :param y: Y轴坐标：1~64
        """

        args = []
        args.append(str(x))
        if y != None:
            args.append(str(y))
        command = 'Pi{}.draw_chart({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def draw_dot(self, x, y):
        """
        

        :param x: X轴坐标：1~128
        :param y: Y轴坐标：1~64
        """

        args = []
        args.append(str(x))
        args.append(str(y))
        command = 'Pi{}.draw_dot({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def draw_line(self, head_x, head_y, tail_x, tail_y):
        """
        在画线的页使用print函数会导致已经画过的线消失切换到不同的页码在回到画线的页码也会导致已经画过的线消失

        :param head_x: 起始点X轴坐标：1~128
        :param head_y: 起始点Y轴坐标：1~64
        :param tail_x: 终止点X轴坐标：1~128
        :param tail_y: 终止点Y轴坐标：1~64
        """

        args = []
        args.append(str(head_x))
        args.append(str(head_y))
        args.append(str(tail_x))
        args.append(str(tail_y))
        command = 'Pi{}.draw_line({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def clear(self):
        """
        

        """

        command = 'Pi{}.clear()'.format(self.index)
        self._set_command(command)

    def set_rgb(self, index, r, g, b):
        """
        0表示控制全部灯

        :param index: 选择灯的序号：0~3  0表示控制全部灯
        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        args = []
        args.append(str(index))
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'Pi{}.set_rgb({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def set_buzzer(self, frequency):
        """
        设置蜂鸣器声音频率（Hz）设置频率为0表示关闭蜂鸣器

        :param frequency: 频率：0~20000 Hz
        """

        args = []
        args.append(str(frequency))
        command = 'Pi{}.set_buzzer({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def play_a_note(self, frequency, time, block=None):
        """
        控制蜂鸣器发出一个音调，并持续一段时间

        :param frequency: 频率：20~20000 Hz
        :param time: 时间: 0.05~60 s
        :param block: 阻塞参数：  False: 不阻塞 True: 阻塞 默认为True
        """

        args = []
        args.append(str(frequency))
        args.append(str(time))
        if block != None:
            args.append(str(block))
        command = 'Pi{}.play_a_note({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def is_a_pressed(self):
        """
        判断按键A是否被按下
        :rtype: bool
        """

        command = 'Pi{}.is_a_pressed()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def is_b_pressed(self):
        """
        判断按键B是否被按下
        :rtype: bool
        """

        command = 'Pi{}.is_b_pressed()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def is_touched(self, pad=None):
        """
        获取某通道是否被触摸
        :rtype: bool
        """

        pad = _format_str_type(pad)

        args = []
        if pad != None:
            args.append(str(pad))
        command = 'Pi{}.is_touched({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return self.val_process(value)

    def get_volume(self):
        """
        声音强度值代表相对强度，值越大代表声音越响
        :rtype: float
        """

        command = 'Pi{}.get_volume()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_light(self, index=None):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: int
        """

        index = _format_str_type(index)

        args = []
        if index != None:
            args.append(str(index))
        command = 'Pi{}.get_light({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value)

    def get_temperature(self):
        """
        获取温度值（°C）
        :rtype: int
        """

        command = 'Pi{}.get_temperature()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_humidity(self):
        """
        获取湿度值(%RH）
        :rtype: int
        """

        command = 'Pi{}.get_humidity()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_air_pressure(self):
        """
        获取气压值(Pa）
        :rtype: int
        """

        command = 'Pi{}.get_air_pressure()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_angle(self, axis=None):
        """
        获取某轴倾斜角，单位°
        :rtype: float
        """

        axis = _format_str_type(axis)

        args = []
        if axis != None:
            args.append(str(axis))
        command = 'Pi{}.get_angle({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value)

    def get_acceleration(self, axis=None):
        """
        获取某轴加速度值，单位g
        :rtype: float
        """

        axis = _format_str_type(axis)

        args = []
        if axis != None:
            args.append(str(axis))
        command = 'Pi{}.get_acceleration({})'.format(self.index,
                                                     ",".join(args))
        value = self._get_command(command)
        return eval(value)

    def reset(self):
        """
        

        """

        command = 'Pi{}.reset()'.format(self.index)
        self._set_command(command)


pi = Pi()
