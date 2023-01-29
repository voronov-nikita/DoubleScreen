import socket
from pyautogui import size

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

IP = "192.168.0.16"
PORT = 9998


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Main"

        self.text_ip_input = TextInput()
        self.text_port_input = TextInput()

        self.Init()

    def Init(self):
        bx = BoxLayout(orientation="vertical")
        btn = Button(text="Connect", )
        btn.bind(on_press=self.the_next_screen)
        bx.add_widget(self.text_ip_input)
        bx.add_widget(self.text_port_input)
        bx.add_widget(btn)
        self.add_widget(bx)

    def the_next_screen(self, *args):
        global IP, PORT
        self.manager.transition.direction = 'right'
        self.manager.current = "Stream"
        IP = self.text_ip_input.text
        PORT = self.text_port_input.text
        return 0

    def on_text(self, instance, value):
        self.on_text.text = print(self.on_text)


class StreamScreen(Screen):
    def __init__(self):
        super().__init__()
        global IP
        global PORT
        self.sock = socket.socket()  # создаем сокет
        self.sock.bind((IP, PORT))  # к серверу
        # self.conn.listen()

        self.name = "Stream"
        x, y = map(int, size())
        self.fl = FloatLayout(size=(x, y))
        self.lbl = Label(text="Text")
        self.Init()

    def Init(self):
        # bxx = BoxLayout(orientation="vertical")
        # if IP is not None or PORT is not None:
        conn = self.sock.accept()
        data = conn.recv(999999)  # Принимаем данные с клиента
        if data:
            print(data)

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(Button(text="exit",
                                  # color="white",
                                  opacity=0.1,
                                  size_hint=(.1, .1),
                                  pos=(.5, .5),
                                  pos_hint={'x': 0, 'y': 0.9},
                                  on_press=self.exit))
        self.add_widget(self.fl)

    def exit(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(StreamScreen())

        return sm


if __name__ == "__main__":
    MainApp().run()
