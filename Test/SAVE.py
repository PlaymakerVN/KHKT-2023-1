# LOG
from pynput.keyboard import Key, Listener
val = []
def on_press(key):
    keys = '{0}'.format(key)
    val.append(keys)
    if keys == 'Key.space' or keys == 'Key.enter':
       for values in val:
         print(values)
       val.clear()
    
    



# Collect events until released
with Listener(
        on_press=on_press) as listener:
    listener.join()