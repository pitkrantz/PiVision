import multiprocessing
from time import sleep
import ctypes

def com_process(ready):
    while True:
        if ready.value == 1:
            for _ in range(50):
                print("kek")
                sleep(0.1)
            ready.value = 0

def main():
    ready = multiprocessing.Value("i", 0)
    instr = multiprocessing.Array(ctypes.c_wchar_p, ["test"])
    process = multiprocessing.Process(target=com_process, args=(ready, instr,))
    process.start()

    while True:
        test = input("Moin: ")
        if test == "1":
            ready.value = 1

if __name__ == "__main__":
    main()