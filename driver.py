import configparser
import os
import threading
import time

import pyautogui
from PIL import ImageGrab
from pynput.keyboard import Key, Listener

from classificator import Classificator


class Driver():

    def __init__(self, image_config, model_config):
        self.config = configparser.ConfigParser()
        self.config.read(image_config, encoding="utf-8")
        self.resized_width = int(self.config["SIZE"]["resized_width"])
        self.resized_height = int(self.config["SIZE"]["resized_height"])
        self.x_top = int(self.config["REGION"]["x_top"])
        self.x_bottom = int(self.config["SIZE"]["width"]) + self.x_top
        self.y_top = int(self.config["REGION"]["y_top"])
        self.y_bottom = int(self.config["SIZE"]["height"]) + self.y_top
        self.classificator = Classificator(model_config)
        self.pressed_key = None
        self.left_sequence_num = 0
        self.left_patience = 2
    

    def forward(self, start_dash=3, boost=0.25, idle=0.3):

        def start_dsah(hold_time):
            pyautogui.keyDown("up")
            time.sleep(hold_time)
            pyautogui.keyUp("up")

        def maintain_speed(boost_time, idle_time):
            while True:
                pyautogui.keyDown("up")
                time.sleep(boost_time)
                pyautogui.keyUp("up")
                time.sleep(idle_time)
        
        start_dsah(hold_time=start_dash)
        maintain_speed(boost_time=boost, idle_time=idle)

    
    def take_picture(self):
        image = ImageGrab.grab()
        image = image.crop(
            (self.x_top, self.y_top, self.x_bottom, self.y_bottom)
        )
        image.resize(size=(self.resized_width*3, self.resized_height*3)).save("log/front_pic.png")
        image = image.resize(size=(self.resized_width, self.resized_height))
        return image


    def handle(self):
        if self.left_sequence_num == self.left_patience:
            print("Sharp curve to left. self.left_patience: " + str(self.left_patience))
            self.left_sequence_num = 0
            self.left_patience = max(1, self.left_patience - 1)
            time.sleep(0.25)
            return
            
        if self.pressed_key is not None:
            pyautogui.keyUp(self.pressed_key)

        image = self.take_picture()
        pred, res = self.classificator.recognize(image)

        if res == 0:
            drive = "straight"
            self.pressed_key = None
            self.left_sequence_num = 0
            self.left_patience = 2
        elif res == 1:
            drive = "left"
            self.pressed_key = "left"
            self.left_sequence_num += 1
        elif res == 2:
            drive = "right"
            self.pressed_key = "right"
            self.left_sequence_num = 0
            self.left_patience = 2
            
        if self.pressed_key is not None:
            pyautogui.keyDown(self.pressed_key)
            
        result_string = "[u:{:.5f} l:{:.5f} r:{:.5f}]".format(pred[0][0], pred[0][1], pred[0][2])
        exp_result = "log/exp_output"
        exp_output_string = "{:.5f}_{:.5f}_{:.5f}_{}".format(pred[0][0], pred[0][1], pred[0][2], drive)
        with open(exp_result, "w") as f:
            f.write(exp_output_string)
        print(drive, result_string, self.left_sequence_num)
    

    def observe(self):
        #start_time = 3
        #for i in range(start_time, -1, -1):
        #    print("\rObserver will be started in {0} sec...".format(i), end="")
        #    time.sleep(1)
        #print()
        self.stop_flag = False
        while self.stop_flag == False:
            self.handle()


if __name__ == "__main__":
    image_config = "config/image_region.ini"
    model_config = "config/train_config.ini"
    dr = Driver(image_config=image_config, model_config=model_config)

    thread_forward = threading.Thread(target=dr.forward)
    thread_observe = threading.Thread(target=dr.observe)

    thread_forward.start()
    thread_observe.start()
