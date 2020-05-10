import sensor,image,lcd,time
import KPU as kpu
import gc

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
clock = time.clock()
classes=  ["aeroplane",  "bicycle", "bird", "boat", "bottle","bus","car","cat","chair","cow","diningtable","dog", "horse", "motorbike", "person", "pottedplant","sheep",  "sofa",   "train",   "tvmonitor"]
#classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
#task = kpu.load(0x500000)
#gc.memfree()
task = kpu.load("/sd/trial2.kmodel")
#task = kpu.load("/sd/20class.kmodel")
#task1 = kpu.load("/sd/lpDet1.kmodel")
#task3 = kpu.load("/sd/weights.kmodel")
#anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
anchor=[0.078, 0.12988, 0.19478, 0.35306,0.77938, 0.83391, 0.61065, 0.40658, 0.33872, 0.68793]
#anchor=[0.196, 0.191, 0.351, 0.393, 0.809,0.674, 0.874, 0.9, 0.684, 0.487]
#anchor=[i*13 for i in anchor]

#a = kpu.init_yolo2(task, 0.4, 0.3, 5, anchor)
a = kpu.init_yolo2(task, 0.5, 0.6, 5, anchor)
while(True):
    clock.tick()
    img = sensor.snapshot()
    #img=img.resize(224,224)

    #task = kpu.load("/sd/20class.kmodel")
    #a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
    code = kpu.run_yolo2(task, img)

    print(clock.fps())
    if code:
        for i in code:
            a=img.draw_rectangle(i.rect(),color=(255,255,0),thickness=3)

            for i in code:
                lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                lcd.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
            img=img.resize(320,240)
            a = lcd.display(img)


    else:
        img=img.resize(320,240)
        a = lcd.display(img)
    #kpu.deinit(task)

a = kpu.deinit(task)
