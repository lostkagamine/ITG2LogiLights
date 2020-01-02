import ctypes
import time
import random
import os
import socket

IP, PORT = "127.0.0.1", 27015 # source engine conflicts, whee
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
print('Successfully bound to 127.0.0.1:27015. Now initialising SDK.')

# In The Groove 2 for Logitech Lightsync-compatible devices
# I had to learn ctypes for this.
# Requires game modification
# (C) 2020 ry00001

codes = {
    'up': 0x148,
    'down': 0x150,
    'left': 0x14B,
    'right': 0x14D,
    'button_left': 0x153,
    'button_right': 0x151,
    'start': 0x1C
}

def get_bit(b, bitNumber):
    return (b & (1 << bitNumber-1)) != 0

def colour(cond, r, g, b):
    if cond:
        return r, g, b
    else:
        return 0, 0, 0

def set_colour(key, cond, r, g, b):
    j, k, l = colour(cond, r, g, b)
    dll.LogiLedSetLightingForKeyWithKeyName(codes[key], j, k, l)

dll_location = os.path.dirname(__file__)
path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "sdk_legacy_led_x86.dll"
print('Loading DLL at '+path)
dll = ctypes.CDLL(path)

print('Attempt to initialise the SDK with python')
ret = dll.LogiLedInit()
print('Success? '+str(ret))
time.sleep(0.25)
print('Done initialising')

# 2,7 = P1 START
# 1,5 = P1 BUTTONS
# 2,1 2,4 2,3 2,2 = P1 LDUR

try:
    while True:
        data, addr = sock.recvfrom(1024)
        data1, data2, data3 = data[0], data[1], data[2]
        print(f'Got something: {data1}, {data2}, {data3}')
        set_colour('start', get_bit(data2,7), 0, 100, 0)
        set_colour('button_left', get_bit(data1,5), 100, 100, 0)
        set_colour('button_right', get_bit(data1,5), 100, 100, 0)

        set_colour('left',get_bit(data2,1),100,100,100)
        set_colour('down',get_bit(data2,4),100,100,100)
        set_colour('up',get_bit(data2,3),100,100,100)
        set_colour('right',get_bit(data2,2),100,100,100)

except KeyboardInterrupt:
    #todo exit cleanly
    print('Quitting')
    exit(0)