import multiprocessing
import ctypes
from time import sleep
multiprocessing.set_start_method("fork")


myArr = multiprocessing.Array(ctypes.c_wchar_p, ["hello", "moin"])
# print(myArr[:])

def addValuetoArr(arr):
    tempArr = myArr[:]
    for i in arr:
        tempArr.append(i) 
    return tempArr

def test():
    print(myArr)  
    sleep(1)
process = multiprocessing.Process(target=test)
while True:
    # myArr = multiprocessing.Array(ctypes.c_wchar_p, addValuetoArr(["hi"]))
    process.start()
    print(myArr[:]) 
    myArr = addValuetoArr(["hi"])
    sleep(1) 
    process.kill()