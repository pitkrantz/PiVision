import threading
from time import sleep
def function_1():
    for i in range(5):
        print("Function 1 is running")
        sleep(0.1) 

def function_2():
    for i in range(5):
        print("Function 2 is running")
        sleep(0.5)
# create two threads for each function
t1 = threading.Thread(target=function_1)
t2 = threading.Thread(target=function_2)

# start the threads
# t1.start()
# t2.start()

# t1.join()
# t2.join()



# Both functions are running simultaneously
# print("Both functions have completed.")
