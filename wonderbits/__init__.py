from .core import *
from .WBPi import pi as Pi  #这个模块会导致串口连接，因为这个模块会定义wonder

from .Tool import wb_tool
from .event import Event
# from .cli import cli

# print(__name__)
# if __name__ == "__main__":
#     cli()
# elif __name__ == "wonderbits":
#     # print('-----------------WonderBits---------------------')
#     pass

# del MyCore
