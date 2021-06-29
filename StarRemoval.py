from tkinter import Tk, filedialog

# Have to do this first because kivy breaks tkinter
window = Tk()
window.withdraw()


import os
from threading import Thread

import kivy
from kivy import Logger
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

import psutil

import starFunctions
from mainScreen import MainScreen

kivy.require('2.0.0')


class StarRemoval(App):
    current_image_path: str = ""
    current_threshold: int = 0

    def build(self):
        Builder.load_file('MainScreen.kv')

        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800
        return SM()

    def get_text(self, path):
        Logger.info(f"Current path set to {path}")
        self.current_image_path = path
        self.root.get_screen("MainScreen").ids["before_image"].source = path

    def threshold(self, thresh):
        Logger.info(f"Current threshold set to {thresh}")
        self.current_threshold = thresh

    def process(self):
        Logger.info("Starting to process image")

        path = self.current_image_path

        if path == "":
            return

        thresh = self.current_threshold
        thresh = float(thresh)


        thread = Thread(target=starFunctions.remove_stars, args=(path, thresh, self.process_finished,
                                                                self.set_processing_text, self.set_stars_amount))
        thread.start()
        self.root.get_screen("MainScreen").ids["process_button"].disabled = True
        self.root.get_screen("MainScreen").ids["after_image"].source = ""



    def process_finished(self, _elapsed_time):
        Logger.info("Finished processing image")
        self.root.get_screen("MainScreen").ids["after_image"].source = str(os.path.splitext(self.current_image_path)[0] + "-no_stars-" + str(self.current_threshold) +
                                                                           os.path.splitext(self.current_image_path)[1])
        self.root.get_screen("MainScreen").ids["after_image"].reload()
        self.root.get_screen("MainScreen").ids["process_button"].disabled = False
        self.root.get_screen("MainScreen").ids["process_label"].text = ""


    def set_processing_text(self, new_text):
        self.root.get_screen("MainScreen").ids["process_label"].text = new_text


    def set_stars_amount(self, stars):
        print(stars)



    def file_explorer(self):
        paths = filedialog.askopenfilenames()
        Logger.debug(f"Paths set to {paths}")
        self.root.get_screen("MainScreen").ids["path_text_input"].text = str(paths[0])


class SM(ScreenManager):
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        self.add_widget(MainScreen(name="MainScreen"))


if __name__ == '__main__':
    Star = StarRemoval()
    Star.run()
