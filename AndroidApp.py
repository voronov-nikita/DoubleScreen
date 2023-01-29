import socket
from pyautogui import size

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


class MainApp(App):

    def build(self):

        x, y = map(int, size())
        fl = FloatLayout(size=(x, y))
        # bxx = BoxLayout(orientation="vertical")
        self.lbl = Label(text="Text")
        fl.add_widget(self.lbl)
        fl.add_widget(Button(text="exit",
                              # color="white",
                              opacity=0.1,
                              size_hint=(.1, .1),
                              pos=(.2, 1),
                              pos_hint={'x':0, 'y':0.9},
                              on_press = self.exit))
        # fl.add_widget(bxx)
        return fl

    def exit(self, instance):
        self.lbl.text = "New Next"


if __name__ == "__main__":
    MainApp().run()
