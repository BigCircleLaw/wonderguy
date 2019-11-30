from .WBits import WBits
from .event import Event


def _format_str_type(x):
    if isinstance(x, str):
        x = str(x).replace('"', '\\"')
        x = "\"" + x + "\""
    return x


class Wonder(WBits):
    def __init__(self, index=1):
        WBits.__init__(self)
        self.index = ''

    def set_onboard_rgb(self, rgb):
        command = 'wonder{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    def print(self, row, column, text):
        """
        在某个位置显示内容

        :param row: 显示行数：1~4
        :param column: 显示列数：1~16
        :param text: 显示内容，可以是字符串，整数，小数
        """

        text = _format_str_type(text)

        args = []
        args.append(str(row))
        args.append(str(column))
        args.append(str(text))
        command = 'wonder{}.print({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def clear(self):
        """
        

        """

        command = 'wonder{}.clear()'.format(self.index)
        self._set_command(command)

    def set_rgb1(self, r, g, b):
        """
        

        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        args = []
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'wonder{}.set_rgb1({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def set_rgb2(self, r, g, b):
        """
        

        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        args = []
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'wonder{}.set_rgb2({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def set_rgb3(self, r, g, b):
        """
        

        :param r: 红色：0~255
        :param g: 绿色：0~255
        :param b: 蓝色：0~255
        """

        args = []
        args.append(str(r))
        args.append(str(g))
        args.append(str(b))
        command = 'wonder{}.set_rgb3({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def set_buzzer(self, frequency):
        """
        设置蜂鸣器声音频率（Hz）设置频率为0表示关闭蜂鸣器

        :param frequency: 频率：0~20000 Hz
        """

        args = []
        args.append(str(frequency))
        command = 'wonder{}.set_buzzer({})'.format(self.index, ",".join(args))
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
        command = 'wonder{}.play_a_note({})'.format(self.index, ",".join(args))
        self._set_command(command)

    def is_a_pressed(self):
        """
        判断按键A是否被按下
        :rtype: bool
        """

        command = 'wonder{}.is_a_pressed()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def is_b_pressed(self):
        """
        判断按键B是否被按下
        :rtype: bool
        """

        command = 'wonder{}.is_b_pressed()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def is_touched(self, pad):
        """
        获取某通道是否被触摸
        :rtype: bool
        """

        pad = _format_str_type(pad)

        args = []
        args.append(str(pad))
        command = 'wonder{}.is_touched({})'.format(self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value)

    def get_volume(self):
        """
        声音强度值代表相对强度，值越大代表声音越响
        :rtype: float
        """

        command = 'wonder{}.get_volume()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_light(self):
        """
        亮度值代表相对强度，值越大代表亮度越强
        :rtype: int
        """

        command = 'wonder{}.get_light()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_x_angle(self):
        """
        获取x轴倾斜角，单位°
        :rtype: float
        """

        command = 'wonder{}.get_x_angle()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_y_angle(self):
        """
        获取y轴倾斜角，单位°
        :rtype: float
        """

        command = 'wonder{}.get_y_angle()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_acceleration(self):
        """
        获取合轴加速度值，单位g
        :rtype: float
        """

        command = 'wonder{}.get_acceleration()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_x_acceleration(self):
        """
        获取x轴轴加速度值，单位g
        :rtype: float
        """

        command = 'wonder{}.get_x_acceleration()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_y_acceleration(self):
        """
        获取y轴轴加速度值，单位g
        :rtype: float
        """

        command = 'wonder{}.get_y_acceleration()'.format(self.index)
        value = self._get_command(command)
        return eval(value)

    def get_z_acceleration(self):
        """
        获取z轴轴加速度值，单位g
        :rtype: float
        """

        command = 'wonder{}.get_z_acceleration()'.format(self.index)
        value = self._get_command(command)
        return eval(value)


wonder = Wonder()
