import utime
import gc
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

# Garbage collector check
gc.enable()
gc.threshold(400000)

# register pin to gpiohs0,
# arg force means force register no matter we have registered before or not
# if arg force=False(by default), register func will return a tuple that registered info,
#                                                           or return number 1
fm.register(board_info.LED_R, fm.fpioa.GPIO0, force=True)
fm.register(board_info.LED_G, fm.fpioa.GPIOHS0, force=True)
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1, force=True)

led_r = GPIO(GPIO.GPIO0, GPIO.OUT)
led_g = GPIO(GPIO.GPIOHS0, GPIO.OUT)
input = GPIO(GPIO.GPIO1, GPIO.IN)

i = 0
status = 0
while i<10:
    led_r.value(status)
    led_g.value(status)
    print("LED :", led_r.value())
    print("loop input:", input.value())
    i+=1
    status = 0 if (status==1) else 1
    utime.sleep_ms(250)

"""Wait for the GPIO input to clean-up garbage
    This is the end of the programm which requires a clean-up IRQ"""

status_1=0 # blik led integer

while input.value() == 1:
    print("Press SW1 to terminate program and clen-up memory:", input.value())
    print("gc.mem_free({})listed" .format(gc.mem_free()))
    led_r.value(status_1)
    status_1 = 0 if (status==1) else 1
    utime.sleep_ms(800)

print("gc.mem_free collector enabled")
if(gc.mem_free()<600000):
    gc.collect()

utime.sleep_ms(500)
print("gc.mem_free collector completed")

utime.sleep_ms(500)

fm.unregister(board_info.LED_R, fm.fpioa.GPIO0)
fm.unregister(board_info.LED_G, fm.fpioa.GPIOHS0)
fm.unregister(board_info.BOOT_KEY, fm.fpioa.GPIO1)
