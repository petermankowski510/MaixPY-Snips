# Edge detection with Canny:
#
# This example demonstrates the Canny edge detector.

import sensor, image, time

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.RGB565
sensor.set_framesize(sensor.QVGA) # or sensor.QVGA (or others)

sensor.set_gainceiling(32)
sensor.set_vflip(1)
sensor.set_hmirror(0)
sensor.run(1)

min_degree = 0
max_degree = 179
clock = time.clock() # Tracks FPS.
white = [255,255,255]

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    img.find_edges(image.EDGE_SIMPLE, threshold=(20, 255))
    #img.cartoon(size=255, seed_threshold=0.05, floating_threshold=0.05, mask=None)

    for c in img.find_lines(threshold = 10000, theta_margin = 15, rho_margin = 15):
           if (min_degree <= c.theta()) and (c.theta() <= max_degree):
               img.draw_line(c.line(), color = white, thickness=10)
               print(c)
               print("Line coordinates: {} are" .format(c.line))


    lcd.display(img)
    print("fps:{}" .format(clock.fps()))
