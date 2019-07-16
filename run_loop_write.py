# import subprocess

# subprocess.check_output(['ampy', '-d', '2', '--port', '/dev/cu.wchusbserial143330' , 'put', 'run_loop.py'])
# subprocess.call(['ampy', '--port', '/dev/cu.wchusbserial143330', 'reset'])


import os
os.system('ampy -d 2 -p /dev/cu.wchusbserial143330  put run_loop.py')
print('download done!')
os.system('ampy -p /dev/cu.wchusbserial143330  reset')
print('soft root done!')

import time
import shutil
print(os.getcwd())
# path = os.path.join(os.getcwd(),'runnn1.py')
# p = shutil.copyfile('run_loop.py', path)
# print(p)
# os.remove(p)