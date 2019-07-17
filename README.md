### 豌豆拼
> 重写了豌豆拼python硬件交互逻辑


```python
from wonderbits import Display, wb_tool, Control, Led
import random
# wb_tool.show_console()

d = Display()
c = Control()
l = Led()

for i in range(20):
    d.print(1,1,i)
    v = c.get_sw4()
    l.set_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    print(v)
```