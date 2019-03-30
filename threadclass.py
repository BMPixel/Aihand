#!usr/bin/python3
import RPi.GPIO as GPIO
import time
import threading

class shakethread (threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)
        self.pin = pin
        self.cnt = 0
        self.maximun = 80
        self.lastnum = 0
        self.start()

    def run(self):
        while True:
            val = GPIO.input(self.pin)
            if val >= 1:
                self.cnt += 1
            time.sleep(0.0008)

    def next_counter(self):
        ret = self.cnt/self.maximun
        tmp = abs(ret - self.lastnum)
        self.lastnum = ret
        ret = tmp
        self.cnt = 0
        return ret


class distancethread (threading.Thread):
    def __init__(self, trig_pin, echo_pin):
        threading.Thread.__init__(self)
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.dist = 0
        self.start()

    def run(self):
        pass
        while True:
            self.dist = self.checkdist()
            time.sleep(0.01)

    def checkdist(self):
        tic = time.time()
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00015)
        GPIO.output(self.trig_pin, GPIO.LOW)
        while not GPIO.input(self.echo_pin):
            if time.time() - tic > 0.1:
                return 1000
            pass
        t1 = time.time()
        while GPIO.input(self.echo_pin):
            if time.time() - tic > 0.1:
                return 1000
            pass
        t2 = time.time()
        return (t2 - t1) * 340 * 100 / 2

# class distancethread (threading.Thread):
#     def __init__(self, trig_pin, echo_pin):
#         threading.Thread.__init__(self)
#         self.trig_pin = trig_pin
#         self.echo_pin = echo_pin
#         self.hist_sum = 0
#         self.hist_num = 0
#         self.start()

#     def run(self):
#         GPIO.output(self.trig_pin, GPIO.HIGH)
#         time.sleep(0.00015)
#         GPIO.output(self.trig_pin, GPIO.LOW)
#         while not GPIO.input(self.echo_pin):
#             pass
#         t1 = time.time()
#         while GPIO.input(self.echo_pin):
#             pass
#         t2 = time.time()
#         self.hist_sum += (t2-t1)*340*100/2
#         self.hist_num += 1
#         print((t2 - t1) * 340 * 100 / 2)

#     def next_counter(self):
#         if self.hist_num > 0:
#             ret = self.hist_sum/self.hist_num
#             self.hist_num = 0
#             self.hist_sum = 0
#             return ret
#         return 0
