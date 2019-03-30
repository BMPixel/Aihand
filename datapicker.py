#!/home/pi/berryconda3/envs/tens/bin/python3
import numpy as np
import RPi.GPIO as GPIO
import threading
import atexit
from threadclass import shakethread, distancethread
from mpu6050 import mpu6050
import json
import time



class processer:
    def __init__(self):
        self.hist = dict()
        self.hist["ax"] = []
        self.hist["ay"] = []
        self.hist["az"] = []
        self.hist["gx"] = []
        self.hist["gy"] = []
        self.hist["gz"] = []
        self.hist["dist"] = []
        self.package = dict()
        self.ck_pin = 17
        self.dis_pin = (27, 10)
        self.thread_shake = None
        self.thread_distance = None
        self.mpudevice = mpu6050(0x68)
        self.lst_info = {}
        self.ori_dict = {}
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.ck_pin, self.dis_pin[1]], GPIO.IN)
        GPIO.setup(self.dis_pin[0], GPIO.OUT, initial=GPIO.LOW)
        time.sleep(0.05)
        atexit.register(self.onexit)
        self.thread_shake = shakethread(self.ck_pin)
        self.thread_distance = distancethread(self.dis_pin[0], self.dis_pin[1])

    def filter_median_que(self, hili, data, length):
        hili.append(data)
        return np.median(hili[-length:])
    
    def get_ori_data(self):
        try:
            self.ori_dict["accel"] = self.mpudevice.get_accel_data()
            self.ori_dict["temp"] = self.mpudevice.get_temp()
            self.ori_dict["gyro"] = self.mpudevice.get_gyro_data()

        except OSError:
            self.ori_dict["accel"] = self.lst_info["accel"]
            self.ori_dict["temp"] = self.lst_info["temp"]
            self.ori_dict["gyro"] = self.lst_info["gyro"]

        self.lst_info["accel"] = self.ori_dict["accel"]
        self.lst_info["temp"] = self.ori_dict["temp"]
        self.lst_info["gyro"] = self.ori_dict["gyro"]
        self.ori_dict["dist"] = self.thread_distance.dist
#         self.ori_dict["dist"] = 8
        self.ori_dict["shake"] = self.thread_shake.next_counter()
        return self.ori_dict

    def get_dict(self, data, length=5):
        self.package["ax"] = self.filter_median_que(self.hist["ax"], data["accel"]["x"],
                                          length)
        self.package["ay"] = self.filter_median_que(self.hist["ay"],
                                               data["accel"]["y"], length)
        self.package["az"] = self.filter_median_que(self.hist["az"],
                                               data["accel"]["z"], length)
        self.package["gx"] = self.filter_median_que(self.hist["gx"],
                                               data["gyro"]["x"], length)
        self.package["gy"] = self.filter_median_que(self.hist["gy"],
                                               data["gyro"]["y"], length)
        self.package["gz"] = self.filter_median_que(self.hist["gz"],
                                               data["gyro"]["z"], length)
        if data["dist"] > 45:
            data["dist"] = 45
        self.package["dist"] = self.filter_median_que(self.hist["dist"],
                                                 data["dist"], length)
        self.package["ax"] = (self.package["ax"] + 6.8) / (5.73 + 6.8)
        self.package["ay"] = (self.package["ay"] - 0.7304) / (7.9687 - 0.7304)
        self.package["az"] = (self.package["az"] - 1.8593) / (9.6406 - 1.8593)
        self.package["gx"] = (self.package["gx"] + 73.7500) / (38.0937 + 73.7500)
        self.package["gy"] = (self.package["gy"] + 104.1875) / (45 + 104.1875)
        self.package["gz"] = (self.package["gz"] + 50.8437) / (45 + 50.8437)
        self.package["dist"] = (self.package["dist"] - 6.6210) / (45 - 6.6210)

        self.package["temp"] = data["temp"]
        self.package["shake"] = data["shake"]

        return self.package
    
    def onexit(self):
        GPIO.cleanup()
    
    def pick_json(self):
        return json.dumps(self.get_ori_data())
        

    def get_array(self, info_dict):
        return np.vstack([
            info_dict['dist'], info_dict['ax'], info_dict['ay'], info_dict['az'], info_dict['gx'],
            info_dict['gy'], info_dict['gz'], info_dict["shake"]
        ]).reshape((1, 8))
    
    def pick_one(self):
        return self.get_array(self.get_dict(self.get_ori_data()))
