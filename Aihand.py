#!/home/pi/berryconda3/envs/tens/bin/python3
import model
import time
import datapicker
import math
import Adafruit_PCA9685
from sys import stdout

print("MSGFinish")
stdout.flush()

step_sec = 12
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
def setpwm(ratio, minimun=135, maximun=355):
    if ratio > 1:
        ratio = 1
    if ratio < 0:
        ratio = 0
    pwm.set_pwm(0, 0, int(ratio * (maximun - minimun) + minimun))

pick = datapicker.processer()

tover = 0
sendable = False
while True:
    tic = time.time()
    ans = model.run(pick.pick_one())
    if sendable >= 4:
        print("NUM%.2f" % (min(5, 1 / abs(ans[0, 0] - 0.5) - 2)))
        sendable = 1
    else:
        sendable += 1
    stdout.flush()
    try:
        setpwm(ans)
    except:
        pass
    while time.time() - tic < 1/step_sec:
        pass
    if (time.time() - tic >= 1 / step_sec + 0.01):
        print("MSGTimeOver")
        stdout.flush()
        # tover -= 1000
