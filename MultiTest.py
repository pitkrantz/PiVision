import multiprocessing
from time import sleep

multiprocessing.set_start_method("fork")

test = multiprocessing.Value("i", 0)

def MainController():
    while True:
        print(test.value)
        if test.value == 1:
            process = multiprocessing.Process(target=subMain)
            process.start()
            process.join()
            process.kill()
            test.value = 0
        sleep(0.01)

def subMain():
    print("Hello")
    sleep(1)
parentProcess = multiprocessing.Process(target=MainController)
parentProcess.start()

while True:
    test.value = 1
    sleep(3)