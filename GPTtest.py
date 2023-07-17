import multiprocessing as mp
from time import sleep

def main(a):
    print(a[:])
    sleep(2)
    a[0] = 1
    a[1] = 2
    for number in a:
       print(number) 

def sub(a):
    print(a[:])
    sleep(2.5)
    print(a[:])

if __name__ == "__main__":
    shared_array = mp.Array("i", 2)

    main_process = mp.Process(target=main, args=(shared_array, ))
    subP = mp.Process(target=sub, args=(shared_array, )) 

    main_process.start()
    subP.start()

    main_process.join()
    subP.join()