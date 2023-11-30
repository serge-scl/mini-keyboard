# Adafruit CircuitPython 8.2.6 on 2023-09-12; Raspberry Pi Pico with rp204
# I used a sensor matrix circuit using diodes; it seems that few people have done this before me.
import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.GP5, board.GP4)
mpr121 = adafruit_mpr121.MPR121(i2c)

map_touch_pyramid = {"03":1, "04":2, "05":3, "06":4, "07":5,
                     "13":6, "14":7, "15":8, "16":9, "17":10,
                     "23":11, "24":12, "25":13, "26":14, "27":15}

start_stop = True

def sens_touch():
    one_num = "_"
    global start_stop
    while start_stop:
        for i in range(4):
            if mpr121[i].value:
                i_num = str(i)
                key_num = one_num + i_num
                kn = key_num[-2:]
                if kn in map_touch_pyramid:
                    nm_tch = map_touch_pyramid[kn]
                    return nm_tch
                    start_stop = False
                print (kn)
                one_num = key_num
                if len(one_num) > 10:
                    start_stop = False
                time.sleep(0.2)

#  sens_touch()
