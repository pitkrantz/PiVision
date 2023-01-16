import serial
import time
arduino = "/dev/cu.usbmodem112101"

ser = serial.Serial(arduino, 9600)

for i in range (0, 255):
    a = str(i)
    ser.write(b"a")
    print(i)
    time.sleep(0.1)

ser.close()