#!/home/pi/berryconda3/envs/tens/bin/python3

import base64
import cv2
import time
import numpy as np
from sys import stdout
from picamera import PiCamera
import io


if __name__ == "__main__":
    with PiCamera() as cam:
        cam.resolution = ((160, 120))
        stream = io.BytesIO()
        for foo in cam.capture_continuous(
                stream, format="jpeg", use_video_port=True):
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            stream.truncate()
            stream.seek(0)
            img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # maxi = img.max()
            # img = cv2.adaptiveThreshold(img,maxi,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
            img = cv2.resize(img, (160, 120))
            img = np.flip(img, 0)
            # img = img[:, :, 2]
            ba = cv2.imencode(".jpeg", img)[1].tostring()
            code = str(base64.b64encode(ba))[2:-1]
            print(code)
            stdout.flush()
            time.sleep(1 / 60)