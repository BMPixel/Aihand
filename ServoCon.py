#!/home/pi/berryconda3/envs/tens/bin/python3
import RPi.GPIO as GPIO
import time
import atexit
import Adafruit_PCA9685
from threading import Thread

class servo_con (Thread):
    def __init__(self):
        Thread.__init__(self)
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.val = 0
        self.alive = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN)

    def setpwm(self, ratio, minimun=135, maximun=340):
        if ratio > 1:
            ratio = 1
        if ratio < 0:
            ratio = 0
        self.pwm.set_pwm(0, 0, int(ratio * (maximun - minimun) + minimun))

    def die(self):
        self.alive = False

    def run(self):
        self.setpwm(self.val)
        while self.alive:
            if GPIO.input(22) == 0:
                self.val += 0.02
            else:
                self.val = 0
            if self.val > 1:
                self.val = 1
            try:
                self.setpwm(self.val)
            except:
                pass
            time.sleep(0.005)