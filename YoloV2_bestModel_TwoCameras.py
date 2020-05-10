#tested with frimware 5-0.22
import sensor,image,lcd
import KPU as kpu

lcd.init(freq=20000000)
sensor.binocular_reset()
#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_pixformat(sensor.GRAYSCALE)
#sensor.set_pixformat(sensor.YUV422)
#sensor.set_framesize(sensor.QVGA)



sensor.shutdown(False)
sensor.set_pixformat(sensor.RGB565)
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






#sensor.set_framesize(sensor.VGA)



#sensor.run(1)
classes=["aeroplane",  "bicycle", "bird",  "boat", "bottle","bus","car","cat","chair","cow","diningtable","dog",  "horse", "motorbike", "person","pottedplant","sheep",  "sofa",   "train",   "tvmonitor"]
task = kpu.load("/sd/best_Y2.kmodel") #change to "/sd/name_of_the_model_file.kmodel" if loading from SD card
#a = kpu.set_outputs(task, 0, 7,7,125) #the actual shape needs to match the last layer shape of your model(before Reshape)
anchor = [0.078, 0.12988, 0.19478, 0.35306, 0.77938, 0.83391, 0.61065, 0.40658, 0.33872, 0.68793]

a = kpu.init_yolo2(task, 0.35, 0.8, 5, anchor) #tweak the second parameter if you're getting too many false positives

try:
 while(True):
    sensor.shutdown(False)
    img = sensor.snapshot()
    #.rotation_corr(z_rotation=180.0)
    #a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)
    if code:
        #print(code)
        for i in code:
           #if i.classid()==11 or i.classid()==8 or i.classid()==10 or i.classid()==12:
           if i.classid()==1 or i.classid()==5 or i.classid()==6 or i.classid()==13:
            print(code)
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0),thickness=4)
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
            #image.cl
        img=img.resize(320,240)
        a = lcd.display(img)

    else:
        img=img.resize(320,240)
        a = lcd.display(img)
    sensor.shutdown(True)
    img = sensor.snapshot()
    #.rotation_corr(z_rotation=180.0)
    #a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)
    if code:
        #print(code)
        for i in code:
           #if i.classid()==11 or i.classid()==8 or i.classid()==10 or i.classid()==12:
           if i.classid()==1 or i.classid()==5 or i.classid()==6 or i.classid()==13:
            print(code)
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0),thickness=4)
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
            #image.cl
        img=img.resize(320,240)
        a = lcd.display(img)

    else:
        img=img.resize(320,240)
        a = lcd.display(img)
    #time.sleep_ms(100)
except:
    print("EXIT AAAAAAAAAAAAAAAAAA")
    a = kpu.deinit(task)

#a = kp
