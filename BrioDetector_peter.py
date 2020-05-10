from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

import sensor,image,lcd
import KPU as kpu
import network
import socket
import gc
from machine import UART

""" Store kpu parameters here  """
def kpu_param_l():
    threshold = 0.7
    nms_num = 0.5
    anchor_num = 5
    anchor=(0.15613, 0.08486, 0.61109,0.64634,0.048207,0.036307,0.32554,0.284185,0.25026,0.11950)
    print("kpu_parameters loaded")

    return(threshold, nms_num, anchor_num, anchor)

## Sensor
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
#sensor.set_vflip(1)
sensor.run(1)

# Garbage collector check
gc.enable()
gc.threshold(400000)
if(gc.mem_free()<600000):
    gc.collect()

classes = ["lp"]

task = kpu.load("/sd/lpOld.kmodel")

""" kpu_param_l()
    Features for the kpu model
    Define your config. only from that file, not locally
    """
threshold, nms_num, anchor_num, anchor = kpu_param_l()

a = kpu.init_yolo2(task, threshold, nms_num, anchor_num, anchor)

while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    print(code)
    if code:
        for i in code:
            a=img.draw_rectangle(i.rect(),color=(255, 255, 0), thickness=3, fill=False) # Changed thickness
            a = img.draw_string(i.x(),i.y(), classes[i.classid()]+":"+str(round(i.value(),2)), color=(0,255,0), scale=2)

        img=img.resize(320,240)
        a = lcd.display(img)
    else:
        img=img.resize(320,240)
        a = lcd.display(img)

a = kpu.deinit(task)
