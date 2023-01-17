import os
file = open("Instructions.gcode", "r")
lines = file.readlines()
print(len(lines))
for line in lines:
    print(bytes(line + "\r\n", "utf-8"))
