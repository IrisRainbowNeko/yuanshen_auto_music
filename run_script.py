import pynput
import time

keyboard_map=[
    ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u'],
]

ctr = pynput.keyboard.Controller()

play_file='./qby.ystone'

def tap(key):
    ctr.press(key)
    ctr.release(key)

time.sleep(3)
with open(play_file) as f:
    lines=f.readlines()
    for x in lines:
        x=eval(x)
        if x[0]=='delay':
            time.sleep(x[1])
        elif x[0]=='note':
            for key in x[1]:
                tap(keyboard_map[key[0]][key[1]])


