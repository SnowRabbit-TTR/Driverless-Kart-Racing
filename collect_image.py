import configparser
import os
import threading
import time

import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Key, Listener

from drive_testor import Driver


PRESS_KEYS = []
COURSE_ID = "s1n"
MODE = "train"
IMAGE_DIR = os.path.join("image", COURSE_ID, MODE)
UP_KEY = Key.up
DOWN_KEY = Key.down
LEFT_KEY = Key.left
RIGHT_KEY = Key.right
IMAGE_WIDTH = 80
IMAGE_HEIGHT = 60
IMAGE_CONFIG = "config/image_region.ini"


class KeyLogger():

    def add_list(self, key):
        try:
            if not key in PRESS_KEYS:
                PRESS_KEYS.append(key)
        except:
            pass
    

    def remove_list(self, key):
        try:
            PRESS_KEYS.remove(key)
        except:
            pass
    

    def on_press(self, key):
        try:
            self.add_list(key)
        except AttributeError:
            self.add_list(key)


    def on_release(self, key):
        self.remove_list(key)

        if key == Key.esc:
            # Stop listener
            return False

    
    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


class ImageCollector():

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding="utf-8")
        self.x_top = int(self.config["REGION"]["x_top"])
        self.x_bottom = int(self.config["SIZE"]["width"]) + self.x_top
        self.y_top = int(self.config["REGION"]["y_top"])
        self.y_bottom = int(self.config["SIZE"]["height"]) + self.y_top
        files = [f for f in os.listdir(IMAGE_DIR) if not f.startswith('.')]
        self.count = len(files)
        print('The number of data in ' + IMAGE_DIR + ' are ' + str(self.count))


    def get_and_save_image(self):
        image = ImageGrab.grab()
        image = image.crop(
            (self.x_top, self.y_top, self.x_bottom, self.y_bottom)
        )
        image = image.resize(size=(IMAGE_WIDTH, IMAGE_HEIGHT))

        u = 1 if UP_KEY in PRESS_KEYS else 0
        d = 1 if DOWN_KEY in PRESS_KEYS else 0
        l = 1 if LEFT_KEY in PRESS_KEYS else 0
        r = 1 if RIGHT_KEY in PRESS_KEYS else 0
        
        file_name = COURSE_ID + '_%07d_%d%d%d%d.png' % (self.count, u, d, l, r)
        file_path = os.path.join(IMAGE_DIR, file_name)
        image.save(file_path)
        self.count += 1
        print("left: " + file_path)
        if l == 1 or r == 1:
            time.sleep(1)
    

    def run(self):
        start_time = 0
        for i in range(start_time, -1, -1):
            print("\rImageCollector will start in {0} sec...".format(i), end="")
            time.sleep(1)
        print()

        stop_flag = False
        while stop_flag == False:
            self.get_and_save_image()
            if Key.esc in PRESS_KEYS:
                print("ImageCollector is stopped.")
                stop_flag = True


if __name__ == "__main__":

    config_file = "config/image_region.ini"
    kl = KeyLogger()
    ic = ImageCollector(config_file)
    dr = Driver()

    maintain_speed = True

    thread_1 = threading.Thread(target=kl.run)
    thread_2 = threading.Thread(target=ic.run)
    if maintain_speed == True:
        thread_3 = threading.Thread(target=dr.run)

    thread_1.start()
    thread_2.start()
    thread_3.start()
