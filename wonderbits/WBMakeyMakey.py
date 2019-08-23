from .WBits import WBits
from .event import Event


def _format_str_type(x):
    if isinstance(x, str):
        x = str(x).replace('"', '\\"')
        x = "\"" + x + "\""
    return x


class MakeyMakey(WBits):
    def __init__(self, index=1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'makeymakey{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    def is_touching(self, channel):
        """
        获取触摸组的某通道是否被触摸
        :rtype: bool
        """

        args = []
        args.append(str(channel))
        command = 'makeymakey{}.is_touching({})'.format(
            self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value)

    def is_mouse_connected(self, channel):
        """
        获取鼠标组的某通道是否被导通
        :rtype: bool
        """

        args = []
        args.append(str(channel))
        command = 'makeymakey{}.is_mouse_connected({})'.format(
            self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value)

    def is_keyboard_connected(self, channel):
        """
        获取键盘组的某通道是否被导通
        :rtype: bool
        """

        args = []
        args.append(str(channel))
        command = 'makeymakey{}.is_keyboard_connected({})'.format(
            self.index, ",".join(args))
        value = self._get_command(command)
        return eval(value)

    @property
    def source_touch(self):
        return self, 'touch', Event._LIST_VALUE_TYPE

    @property
    def source_mouse(self):
        return self, 'mouse', Event._LIST_VALUE_TYPE

    @property
    def source_keyboard(self):
        return self, 'keyboard', Event._LIST_VALUE_TYPE
