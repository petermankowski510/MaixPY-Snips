#tested with frimware 5-0.22

from Maix import GPIO
from board import board_info
from fpioa_manager import fm

import sensor,image,lcd, utime, gc
import KPU as kpu

# register pin to gpiohs0,
# arg force means force register no matter we have registered before or not
# if arg force=False(by default), register func will return a tuple that registered info,
#                                                           or return number 1
fm.register(board_info.LED_R, fm.fpioa.GPIO0, force=True)
fm.register(board_info.LED_G, fm.fpioa.GPIOHS0, force=True)
#fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1, force=True)

led_r = GPIO(GPIO.GPIO0, GPIO.OUT)
led_g = GPIO(GPIO.GPIOHS0, GPIO.OUT)
#input = GPIO(GPIO.GPIO1, GPIO.IN)

lcd.init(freq=20000000)

""" lcd orientation set-up"""
lcd.direction(lcd.YX_RLUD)

sensor.binocular_reset()

sensor.shutdown(False)
sensor.set_pixformat(sensor.RGB565)
#sensor.set_pixformat(sensor.GRAYSCALE)
#sensor.set_pixformat(sensor.YUV422)
#sensor.set_framesize(sensor.QVGA)

sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))

sensor.set_vflip(1)
sensor.set_hmirror(0)

sensor.shutdown(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.set_hmirror(0)
sensor.run(1)

classes=["aeroplane",  "bicycle", "bird",  "boat", "bottle","bus","car","cat","chair","cow","diningtable","dog",  "horse", "motorbike", "person","pottedplant","sheep",  "sofa",   "train",   "tvmonitor"]
task = kpu.load("/sd/best_Y2.kmodel") #change to "/sd/name_of_the_model_file.kmodel" if loading from SD card

anchor = [0.078, 0.12988, 0.19478, 0.35306, 0.77938, 0.83391, 0.61065, 0.40658, 0.33872, 0.68793]

a = kpu.init_yolo2(task, 0.35, 0.8, 5, anchor) #tweak the second parameter if you're getting too many false positives

status = 0

try:
 while(True):
    sensor.shutdown(False)
    img = sensor.snapshot()
    #.rotation_corr(z_rotation=180.0)
    #a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)

    if code:
        for i in code:
           if i.classid()==1 or i.classid()==5 or i.classid()==6 or i.classid()==13:
            print(code)
            status = 0 if (status==1) else 1
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0),thickness=10)
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
            led_r.value(status)
            led_g.value(status)

        img=img.resize(320,240)
        a = lcd.display(img)

    else:
        img=img.resize(320,240)
        a = lcd.display(img)
    sensor.shutdown(True)
    img = sensor.snapshot()
    #.rotation_corr(z_rotation=180.0)
    code = kpu.run_yolo2(task, img)
    if code:
        led_r.value(0)
        for i in code:
           if i.classid()==1 or i.classid()==5 or i.classid()==6 or i.classid()==13:
            print(code)
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0),thickness=10)
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
        img=img.resize(320,240)
        a = lcd.display(img)

    else:
        img=img.resize(320,240)
        a = lcd.display(img)

except:
    print("EXIT Two Camera Mode")
    a = kpu.deinit(task)
    led_r.value(1)
    print("gc.mem_free collector enabled")
    if(gc.mem_free()<600000):
        gc.collect()

    fm.unregister(board_info.LED_R, fm.fpioa.GPIO0)
    fm.unregister(board_info.LED_G, fm.fpioa.GPIOHS0)
    #fm.unregister(board_info.BOOT_KEY, fm.fpioa.GPIO1)
