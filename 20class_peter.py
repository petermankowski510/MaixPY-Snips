"""April 27, 2020 Rev.
    Author: Andrei
    Modifier: Peter"""

import sensor,image,lcd,time
import KPU as kpu
import gc

# Garbage collector check
gc.enable()
gc.threshold(400000)

""" Store kpu parameters here  """
def kpu_param_l():
    threshold = 0.7
    nms_num = 0.5
    anchor_num = 5
    anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    print("kpu_parameters loaded")

    return(threshold, nms_num, anchor_num, anchor)

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)

clock = time.clock()

classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

task = kpu.load("/sd/20class.kmodel")

#anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

#a = kpu.init_yolo2(task, 0.4, 0.5, 5, anchor)

""" kpu_param_l()
    Features for the kpu model
    Define your config. only from that file, not locally
    """
threshold, nms_num, anchor_num, anchor = kpu_param_l()

a = kpu.init_yolo2(task, threshold, nms_num, anchor_num, anchor)

while(True):
    clock.tick()
    img = sensor.snapshot()

    code = kpu.run_yolo2(task, img)

    print("Clock speed ", clock.fps())
    if code:
        for i in code:
            print(code)
            """ Boxing object class here"""
            a=img.draw_rectangle(i.rect(), color=(255, 255, 0), thickness=5, fill=False)
            a = lcd.display(img)

            for i in code:
                lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                lcd.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
    else:
        a = lcd.display(img)

a = kpu.deinit(task)

if(gc.mem_free()<600000):
    gc.collect()
