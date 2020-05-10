import sensor, lcd
from Maix import utils

utils.gc_heap_size(1000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.run(1)
sensor.skip_frames()
lcd.init(freq=15000000)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot().compress(quality=20)
    print("fps:", clock.fps())
