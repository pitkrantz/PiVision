import serial
import time

printerPort = "/dev/cu.usbserial-A10JYZY0"

ser = serial.Serial(printerPort, 115200)

time.sleep(1)

ser.write(b'G106 S255 \r\n')
ser.write(b'G4 P5000 \r\n')
time.sleep(2)
ser.close()