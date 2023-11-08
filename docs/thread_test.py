import threading
import time
import sys

_looping = True
class MyThreadedClass1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.value = None

    def run(self):
        global _looping
        while _looping:
            # run loop here
            self.value = 1
            time.sleep(1)

class MyThreadedClass2(threading.Thread):
    def __init__(self, thread1):
        threading.Thread.__init__(self)
        self.value = None

    def run(self):
        global _looping
        while _looping:
            # run loop here
            self.value = 2
            time.sleep(1)

def main():
    
    try:
        # init MyThreadedClass1 here
        thread1 = MyThreadedClass1()
        thread1.start()

        # init MyThreadedClass2 here
        thread2 = MyThreadedClass2()
        thread2.start()

    # Main loop that prints "Hello"
        while True:
            print("Hello")
            print(thread1.value)
            print(thread2.value)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, terminating threads")
        global _looping
        _looping = False
        thread1.join()
        thread2.join()
        # sys.exit(0)

if __name__ == "__main__":
    main()
