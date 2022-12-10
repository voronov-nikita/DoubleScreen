from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image
from kivy.core import audio
from kivy.core.audio import SoundLoader

import socket
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')


# I set the color constants to then color the text on the buttons (this is optional)
red = (255 / 255, 67 / 255, 67 / 255)
green = (0 / 255, 158 / 255, 60 / 255)


class MainApp(App):
    def build(self):
        # here I add the main and second screens to the manager, this class does nothing else
        sm.add_widget(MainScreen())
        sm.add_widget(SecondScreen())
        return sm  # I return the manager to work with him later


class MainScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Main'  # setting the screen name value for the screen manager
        # (it's more convenient to call by name rather than by class)

        main_layout = FloatLayout()  # creating an empty layout that's not bound to the screen

        self.add_widget(main_layout)  # adding main_layout on screen

        # Button
        Go_Screen2 = Button(text='Go to Screen2',
                            size_hint=(.5, .5),
                            pos_hint={'center_x': .5, 'center_y': .5},
                            color=red)

        Go_Screen2.bind(on_press=self.to_second_scrn)  # setting up a button to perform an action when clicked

        main_layout.add_widget(Go_Screen2)  # adding button on layout

    def to_second_scrn(self, *args):
        self.manager.current = 'Second'  # selecting the screen by name (in this case by name "Second")
        return 0  # this line is optional


class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Second'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        # Button
        Go_Back = Button(text='Go to Main screen',
                         size_hint=(.5, .5),
                         pos_hint={'center_x': .5, 'center_y': .5},
                         color=green)

        Go_Back.bind(on_press=self.to_main_scrn)

        second_layout.add_widget(Go_Back)

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0


sm = ScreenManager()  # it's necessary to create a manager variable that will collect screens and manage them

if __name__ == '__main__':
    MainApp().run()