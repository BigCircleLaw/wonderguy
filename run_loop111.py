from wonderbits import Display
import time
d = Display()
for i in range(400):
    d.print(1,1,'hello {}'.format(i))
