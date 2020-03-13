from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class Acceleration(WBits):
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'acceleration{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def get_x_angle(self):
        """
        获取x轴倾斜角，单位°
        :rtype: float
        """

        command = 'acceleration{}.get_x_angle()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_y_angle(self):
        """
        获取x轴倾斜角，单位°
        :rtype: float
        """

        command = 'acceleration{}.get_y_angle()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def calibrate(self, block = None):
        """
        注意：校准过程中需确保加速度模块且保持静止不动，有汉字的一面朝上。校准时，模块指示灯会变为黄色，等待指示灯变蓝说明校准完成了。

        :param block: 阻塞参数：  False表示不阻塞 True表示阻塞
        """

        
        args = []
        if block != None:
            args.append(str(block))
        command = 'acceleration{}.calibrate({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_x_acceleration(self):
        """
        获取x轴加速度值，单位m/s2
        :rtype: float
        """

        command = 'acceleration{}.get_x_acceleration()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_y_acceleration(self):
        """
        获取y轴加速度值，单位m/s2
        :rtype: float
        """

        command = 'acceleration{}.get_y_acceleration()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_z_acceleration(self):
        """
        获取z轴加速度值，单位m/s2
        :rtype: float
        """

        command = 'acceleration{}.get_z_acceleration()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_acceleration(self):
        """
        获取x、y、z轴合加速度值，单位m/s2
        :rtype: float
        """

        command = 'acceleration{}.get_acceleration()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_x_angular_velocity(self):
        """
        获取x轴角速度值，单位°/s
        :rtype: float
        """

        command = 'acceleration{}.get_x_angular_velocity()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_y_angular_velocity(self):
        """
        获取y轴角速度值，单位°/s
        :rtype: float
        """

        command = 'acceleration{}.get_y_angular_velocity()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def get_z_angular_velocity(self):
        """
        获取z轴角速度值，单位°/s
        :rtype: float
        """

        command = 'acceleration{}.get_z_angular_velocity()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        

    
    @property
    def source_x_acceleration(self):
        return self, 'x_acceleration', []
    
    @property
    def source_y_acceleration(self):
        return self, 'y_acceleration', []
    
    @property
    def source_z_acceleration(self):
        return self, 'z_acceleration', []
    
    @property
    def source_x_angular_velocity(self):
        return self, 'x_angular_velocity', []
    
    @property
    def source_y_angular_velocity(self):
        return self, 'y_angular_velocity', []
    
    @property
    def source_z_angular_velocity(self):
        return self, 'z_angular_velocity', []
    
    @property
    def source_x_angle(self):
        return self, 'x_angle', []
    
    @property
    def source_y_angle(self):
        return self, 'y_angle', []
    
    @property
    def source_acceleration(self):
        return self, 'acceleration', []
    

    def when_x_tilted(self):
        return Event(self.source_x_angle, 'abs(x)>10')


    def when_y_tilted(self):
        return Event(self.source_y_angle, 'abs(x)>10')


    