import serial
import pygcode
from time import sleep

#printerPort = "/dev/tty.usbserial-1210"
printerPort = "/dev/cu.usbserial-A10JYZY0" #normal
#printerPort = "/dev/cu.usbserial-1230"

ser = serial.Serial(printerPort, 115200)


#ser.write(b'G0 Z20 \r\n')
#ser.write(b'M107 \r\n')
ser.write(b'G4 P2000 \r\n')
ser.write(b'M106 S255 \r\n')

#ser.write(b'G28 \r\n')
#ser.write(b'G0 Z20 \r\n')
#ser.write(b'G4 P10000\r\n')
#ser.write(b'G0 X10 \r\n')
#ser.write(b'M106 S255 \r\n')
#ser.write(b'G0 Y20 X20 \r\n')
#ser.write(b'G0 Y20 \r\n')
#ser.write(b'M107\r\n')
#ser.write(b'M107 \r\n')

sleep(1)
ser.close()