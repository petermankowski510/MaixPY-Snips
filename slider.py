import time
import struct
import math
import gc
import image
import lcd
import time

lcd.init()

img = image.Image(copy_to_fb=0)

sigX=50
wX=50
clr=120
peak=125

while True:
  for clr in range(255):
    colorI=(clr,255-clr,255-clr)
    wX=clr
    img.draw_rectangle(int(sigX),0,wX,peak,fill=True,color=colorI)

    #### Emulates blink ####
    if (clr+1)%4==0:
        dots="".join(["."]*int(clr/30))
        img.draw_string(0,40+65*2, ("Drawing"+dots), color=(0,255,255), scale=2.5)

    else:
        img.draw_string(0,40+65*2, ("                              "), color=(0,255,255), scale=2)

    lcd.display(img)

    #### Needed for smooth blink ####
    if (clr+1)%12==0:
        img.clear()

  img.clear()


