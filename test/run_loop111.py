from wonderbits import Display
import time
d = Display()
count = 0;
while True:
    d.print(1,1,'hello {}'.format(count))
    count = count + 1
