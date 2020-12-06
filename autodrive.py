import os

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ListProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.boxlayout import BoxLayout

Config.set("graphics", "width", "500")
Config.set("graphics", "height", "400")
Config.set("graphics", "resizable", False)

kv = """
<AutoDriveBoard>:
    front_image: front_image
    operate_image: operate_image

    BoxLayout:
        canvas:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                size: self.size
                pos: self.pos
        orientation: "vertical"

        Image:
            size_hint_y: 0.4
            id: operate_image
            source: root.operate_image_path

        BoxLayout:
            size_hint_y: 0.4
            orientation: "horizontal"

            Image:
                size_hint_x: 0.4
                id: front_image
                source: root.front_image_path

            Image:
                size_hint_x: 0.3
                font_size: 32
                source: "resource/cnn.png"

            BoxLayout:
                size_hint_x: 0.3
                orientation: "vertical"
                BoxLayout:
                    Label:
                        size_hint_x: 0.4
                        text: "straight"
                        color: 0, 0, 0, 1
                    Label:
                        size_hint_x: 0.6
                        text: root.output_per[0]
                        color: 0, 0, 0, 1
                BoxLayout:
                    Label:
                        size_hint_x: 0.4
                        text: "left"
                        color: 0, 0, 0, 1
                    Label:
                        size_hint_x: 0.5
                        text: root.output_per[1]
                        color: 0, 0, 0, 1
                BoxLayout:
                    Label:
                        size_hint_x: 0.4
                        text: "right"
                        color: 0, 0, 0, 1
                    Label:
                        size_hint_x: 0.5
                        text: root.output_per[2]
                        color: 0, 0, 0, 1

        Button:
            size_hint_y: 0.2
            font_size: 20
            text: root.button_text
            color: root.string_color
            on_press: root.switch()

"""

Builder.load_string(kv)


class AutoDriveBoard(BoxLayout):

    front_image = ObjectProperty(None)
    operate_image = ObjectProperty(None)
    operate_image_path = StringProperty()
    button_text = StringProperty()
    output_per = ListProperty([])
    string_color = ListProperty()


    def __init__(self, **kwargs):
        self.front_image_path = "log/front_pic.png"
        self.operate_image_path = "resource/neutral.png"
        self.output_per = ["0.00000", "0.00000", "0.00000"]
        self.button_text = "Mode: Manual operation"
        self.is_monitor = False
        self.red_string = [1, 0.5, 0.5, 1]
        self.blue_string = [0.5, 0.5, 1, 1]
        self.string_color = self.blue_string

        cp_command_1 = "cp log/exp_output_start log/exp_output"
        cp_command_2 = "cp log/front_pic_start.png log/front_pic.png"
        os.system(cp_command_1)
        os.system(cp_command_2)

        super(AutoDriveBoard, self).__init__(**kwargs)


    def switch(self):
        if self.is_monitor == False:
            self.is_monitor = True
            self.button_text = "Mode: Automatic operation"
            self.string_color = self.red_string
            Clock.schedule_interval(self.update_resource, 1.5)
        else:
            self.is_monitor = False
            self.button_text = "Mode: Manual operation"
            self.string_color = self.blue_string


    def update_resource(self, dt):
        self.front_image.reload()

        with open("log/exp_output") as f:
            exp_output = f.read().strip("\n")
            p_straight, p_left, p_right, key = exp_output.split("_")
            self.output_per = [str(p_straight), str(p_left), str(p_right)]
            self.operate_image_path = "resource/{}.png".format(key)
            self.operate_image.reload()


class AutoDriveApp(App):

    def build(self):
        return AutoDriveBoard()


if __name__ == "__main__":
    AutoDriveApp().run()
