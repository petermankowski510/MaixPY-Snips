from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

import sensor,image,lcd
import KPU as kpu
import network
import socket
from machine import UART

## Sensor
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
classes = ["lp"]
#task = kpu.load("/sd/weights.kmodel")
#task = kpu.load("/sd/lpDet1.kmodel")
#task = kpu.load("/sd/lpProper.kmodel")
task = kpu.load("/sd/lpOld.kmodel")
#task1 = kpu.load(0x500000)
anchor=(0.15613, 0.08486, 0.61109,0.64634,0.048207,0.036307,0.32554,0.284185,0.25026,0.11950)
#anchor=(13*0.15613, 13*0.08486, 13*0.61109,13*0.64634,13*0.048207,13*0.036307,13*0.32554,13*0.284185,13*0.25026,13*0.11950)
#anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
#a = kpu.init_yolo2(task, 0.3, 0.7, 5, anchor)
a = kpu.init_yolo2(task, 0.7, 0.5, 5, anchor)

while(True):
    img = sensor.snapshot()
    #img=img.resize(320,240)
    code = kpu.run_yolo2(task, img)
    #img=img.resize(320,240)
    print(code)
    if code:
        for i in code:
            a=img.draw_rectangle(i.rect(),color = (255, 255, 0))
            a = img.draw_string(i.x(),i.y(), classes[i.classid()]+":"+str(round(i.value(),2)), color=(255,0,0), scale=2)
            #http_get('http://192.168.178.29/train/1')
        img=img.resize(320,240)
        a = lcd.display(img)
    else:
        img=img.resize(320,240)
        a = lcd.display(img)
a = kpu.deinit(task)
