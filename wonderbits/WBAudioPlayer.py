from .WBits import WBits
from .event import Event

def _format_str_type(x):
    if isinstance(x, str):
       x = str(x).replace('"', '\\"')
       x = "\"" + x + "\""
    return x

class AudioPlayer(WBits):
    LOOP_PLAY = 0
    SINGLE_LOOP = 2
    RANDOM_PLAY = 3
    SINGLE_PLAY = 4
    def __init__(self, index = 1):
        WBits.__init__(self)
        self.index = index

    def set_onboard_rgb(self, rgb):
        command = 'audioPlayer{}.set_onboard_rgb({})'.format(self.index, rgb)
        self._set_command(command)

    
    def play(self):
        """
        如果是上电后直接调用此函数会播放导入的第一首音乐如果是暂停之后调用此函数则会继续播放

        """

        command = 'audioPlayer{}.play()'.format(self.index)
        self._set_command(command)

    
    def play_by_name(self, name = None):
        """
        参数为音乐名，前三个字符必须是该音乐的文件名序号

        :param name: 音乐名
        """

        name = _format_str_type(name)
        
        args = []
        if name != None:
            args.append(str(name))
        command = 'audioPlayer{}.play_by_name({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def pause(self):
        """
        将正在播放的歌曲暂停

        """

        command = 'audioPlayer{}.pause()'.format(self.index)
        self._set_command(command)

    
    def next(self):
        """
        播放下一首音乐

        """

        command = 'audioPlayer{}.next()'.format(self.index)
        self._set_command(command)

    
    def previous(self):
        """
        播放上一首音乐

        """

        command = 'audioPlayer{}.previous()'.format(self.index)
        self._set_command(command)

    
    def set_volume(self, volume):
        """
        设置播放音乐的音量

        :param volume: 音量：0~100
        """

        
        args = []
        args.append(str(volume))
        command = 'audioPlayer{}.set_volume({})'.format(self.index, ",".join(args))
        self._set_command(command)

    
    def get_name(self):
        """
        获取正在播放的音乐名称
        :rtype: str
        """

        command = 'audioPlayer{}.get_name()'.format(self.index)
        value = self._get_command(command)
        return value
        
    def get_progress(self):
        """
        获取正在播放音乐的播放进度
        :rtype: int
        """

        command = 'audioPlayer{}.get_progress()'.format(self.index)
        value = self._get_command(command)
        return self.val_process(value)
        
    def replay(self):
        """
        如果正在播放的音乐调用此函数会重新播放该音乐如果当前没有播放音乐调用此函数会播放之前播放的一首

        """

        command = 'audioPlayer{}.replay()'.format(self.index)
        self._set_command(command)

    
    def set_mode(self, mode):
        """
        设置播放器的播放模式

        :param mode: 播放模式  LOOP_PLAY: 循环播放 SINGLE_LOOP: 单曲循环 RANDOM_PLAY: 随机播放 SINGLE_PLAY: 单曲播放
        """

        
        args = []
        args.append(str(mode))
        command = 'audioPlayer{}.set_mode({})'.format(self.index, ",".join(args))
        self._set_command(command)

    

    
    @property
    def source_song_index(self):
        return self, 'song_index', []
    

    def when_playing_finished(self):
        return Event(self.source_song_index, Event.TRIGGER_TRUE_TO_FALSE)


    