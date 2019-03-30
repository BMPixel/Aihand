#!/home/pi/berryconda3/envs/tens/bin/python3
import time
from sys import stdout
import datapicker


if __name__ == "__main__":
    pick = datapicker.processer()
    while True:
        time.sleep(1 / 12)
        print(pick.pick_json())
        stdout.flush()