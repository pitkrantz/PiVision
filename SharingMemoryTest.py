import multiprocessing
import ctypes
from time import sleep
import threading

ready = multiprocessing.Value("i", 0)

def COM():
    while True:
        if ready.value == 1:
            while True:
                for i in range(0,10):
                    print("kek")
                ready.value = 0

def main():
    sub_thread = threading.Thread(target=COM)
    sub_thread.daemon = True
    sub_thread.start()
    while True:
        test = input("Moin")
        if test == "1":
            ready.value = 1

if __name__ == "__main__":
    main()