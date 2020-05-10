from fpioa_manager import fm
from machine import UART
from board import board_info
import time

def checkSum(data):
    carry = 0
    for input in data:
        if input==0x55: continue
        if ((input + carry)&0xFFFF) < carry:
            carry = (carry + input + 1)&0xFFFF
        else:
            carry = (carry+input)&0xFFFF
        if(carry > 0x00FF):
            carry = (carry-255)&0xFFFF
    carry = ~carry & 0x00FF
    data.append(carry)

#command table w conversion
thresholds = [0x55,0x19,0x97,0x99,0x99,0x99,0x99,0x9a,0xF9,0x04,0x21,0x08,0x64,0x31,0x3b,0x45,0x4f,0x07,0x77,0x77,0x77,0x77,0x78,0x88,0x9c,0xd0,0x72,0x10,0x63,0x28,0x30,0x34,0x3c,0x0]
thresholds = bytearray(thresholds)
checkSum(thresholds)

sendPulse = [0x55,0x11,0x01]
sendPulse = bytearray(sendPulse)
checkSum(sendPulse)

getDataL = [0x55,0x05]
getDataL = bytearray(getDataL)
checkSum(getDataL)

fm.register(board_info.PIN15, fm.fpioa.UART3_TX, force=True)
fm.register(board_info.PIN17, fm.fpioa.UART3_RX, force=True)

uart_3 = UART(UART.UART3, 115200,8,0,2, timeout=10, read_buf_len=4096)

uart_3.write(thresholds)
while 1:
    uart_3.write(sendPulse)
    time.sleep_ms(40)
    uart_3.write(getDataL)
    receivedData = uart_3.read()
    distance = (receivedData[1]<<8 | receivedData[2])*0.01715
    print(distance)



uart_3.deinit()
del uart_3
