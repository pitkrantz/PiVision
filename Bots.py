class SerialManager:
    def __init__(self):
        self.ser = serial.Serial(robotPort, 115200)
        sleep(3)
        response = self.ser.readline()
        if response == b"\r\n":
            response = self.ser.readline()
        #print(response)
        print("Connected")
        # self.ser.write(b'G28 \r\n')
        # output = self.ser.readline()
        # if output == b"ok\r\n":
        #     print("ok") 
        #     pass
        # else:
        #     print("Error")
        #     return
    
    def executeArr(self, array):

        #I think I will use this method in order to not put to much strain on the SSd by creating and deleting files + speed


        print("executing")
        for line in array:
            self.ser.write(bytes(line, "utf-8"))
            output = self.ser.readline()
            print(output)
            sleep(0.1)

        InstructionsArr = []


        #!!!!! Always close a file before reading it somewhere else, because this saves the acutal data
    def executeFile(self):
        currentFile = open("Instructions.gcode", "r")
        instructions = currentFile.readlines()
        print("file is being read")
        print(len(instructions))
        #print(instructions)
        #print(bytes(instructions[2], "utf-8"))
        for i in range(0, (len(instructions))):
            print(i)
            print(bytes(instructions[i], "utf-8"))
            self.ser.write(bytes(instructions[i], "utf-8"))
            output = self.ser.readline()
            if output == b"ok\r\n":
                print("ok")
            else:
                print(output)     
            sleep(0.2) 
        # print("deleting file")
        # os.remove("Instructions.gcode")
    
    def closeSerial(self):
        self.ser.close()

class GcodeGenerator:

    def __init__(self):
        self.Connection = serialmanager

    def newModelTest(self):
        InstructionsArr.append("G0 X100\r\n")
        InstructionsArr.append("G0 X200\r\n")

    def lineTest(self):
        file = open("Instructions.gcode", "w")
        InstructionsArr.append("G0 X100 Y100\r\n") # move the pen of to the middle a bit
        InstructionsArr.append("M4 S100\r\n")#pen down
        InstructionsArr.append("G4 P1000\r\n")
        InstructionsArr.append("G1 X20\r\n")
        InstructionsArr.append("G1 Y20\r\n")
        InstructionsArr.append("M5\r\n")
        print("Testline File created")
        file.close()

    
    def penDown(self):
        #print("Starting Pen Down")
        #file = open("Instructions.gcode", "w")
        InstructionsArr.append("M4 S100\r\n")
        InstructionsArr.append("G4 P1\r\n")
        InstructionsArr.append("M5\r\n")

    def calibrate(self):
        print("calibrating...")
        file = open("Instructions.gcode", "w")
        InstructionsArr.append("G28\r\n")
        InstructionsArr.append("G0\r\n")
        print("Calibration File created")
        file.close() 

    def cross(self, centerPoint):
         
        print("Cross")
        # this function draws a cross starting TL to BR -> BL to TR
        half_squareLength = squareLength/2
        InstructionsArr.append("G0 X" + str(centerPoint[0] - half_squareLength)+ " Y" + str(centerPoint[1] + half_squareLength) + "\r\n")
        InstructionsArr.append("M4 S100\r\n") # set pen down
        InstructionsArr.append("G1 X" + str(centerPoint[0] + (half_squareLength)) + " Y" + str(centerPoint[1] - half_squareLength) + "\r\n")
        InstructionsArr.append("M5\r\n") # lift pen move to lower left corner 
        InstructionsArr.append("G0 X" + str(centerPoint[0] - half_squareLength) + " Y" + str(centerPoint[1] - half_squareLength) + "\r\n")
        InstructionsArr.append("M4 S100\r\n")# set pen down
        InstructionsArr.append("G1 X" + str(centerPoint[0]+ half_squareLength) + " Y" + str(centerPoint[1] + half_squareLength) + "\r\n")
        InstructionsArr.append("M5\r\n") # lift pen up
        InstructionsArr.append("G0 X0 Y0" + "\r\n") 
    
    def drawPlayingField():
        print("Setting up...")