#!/home/pi/berryconda3/envs/tens/bin/python3
import time
import json
import io
import csv
import ServoCon
import datapicker
import numpy as np
import atexit

# main function
if __name__ == "__main__":

    servo = ServoCon.servo_con()
    servo.start()
    atexit.register(servo.die)
    process = datapicker.processer()

    filename = "/home/pi/Desktop/Workspace/train_data/" + time.strftime(
        "%H:%M:%S_%d") + '.csv'
    with open(filename, "w") as f:
        writer = csv.writer(f)
        # write first line
        writer.writerow([
            "ax", "ay", "az", "gx", "gy", "gz", "dist", "temp", "shake",
            "state"
        ])
        while True:
            try:
                str_json = input()
                data = json.loads(str_json)
                package = process.get_dict(data)
                package["state"] = servo.val

                writer.writerow([
                    package["ax"], package["ay"], package["az"], package["gx"],
                    package["gy"], package["gz"], package["dist"],
                    package["temp"], package["shake"], package["state"]
                ])
                
            except:
                servo.die()
                break
