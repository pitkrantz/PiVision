import serial
import pygcode
from time import sleep

printerPort = "/dev/tty.usbserial-1210"


ser = serial.Serial(printerPort, 115200)

sleep(2)
ser.write(b'G0 Z20 \r\n')
sleep(1)
ser.close()