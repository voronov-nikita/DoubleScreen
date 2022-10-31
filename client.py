from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread
from kivy.uix.image import Image

import socket
import threading

KV = """
MyBL:

    orientation:"vertical"
    size_hint:(0.95, 0.95)
    pos_hint:{"center_x": 0.5, "center_y":0.5}

    Label:
        font_size: "20sp"
        multiline:True
        size_hint_x:1
        size_hint_y:None
        height: self.texture_size[1]
        text: root.data_label
        
    TextInput:
        id: Inp
        multiline: False
        padding_y: (5,5)
        size_hint: (1, 0.20)
        
    
    Button:
        text: "google"
        bold : True
        background_color:'#000080'
        size_hint: (1, 0.25)
        on_press: root.click1()
        
    Button:
        text: "мэш"
        bold : True
        background_color:'#000080'
        size_hint: (1, 0.25)
        on_press: root.click2()
        
    Button:
        text: "youtube"
        bold : True
        background_color:'#000080'
        size_hint: (1, 0.25)
        on_press: root.click3()
        
    Button:
        text: "vk"
        bold : True
        background_color:'#000080'
        size_hint: (1, 0.25)
        on_press: root.click4()
"""


class MyBL(BoxLayout):
    data_label = StringProperty("Подключено!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SERVER = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
        PORT = 4321

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.client.sendall(bytes("979879789", 'UTF-8'))

        threading.Thread(target=self.get_data).start()

    def click1(self):
        self.client.sendall(bytes("google", 'UTF-8'))

    def click2(self):
        self.client.sendall(bytes("мэш", 'UTF-8'))

    def click3(self):
        self.client.sendall(bytes("youtube", 'UTF-8'))

    def click4(self):
        self.client.sendall(bytes("vk", 'UTF-8'))

    def get_data(self):
        while App.get_running_app().running:
            in_data = self.client.recv(4096)
            print("От сервера:", in_data.decode())
            kkk = in_data.decode()
            self.set_data_label(kkk)

    @mainthread
    def set_data_label(self, data):
        self.data_label += str(data) + "\n"


class ErrorApp(App):
    image = True
    txt1 = "Ошибка сервера, немного подождите"

    def error_event(self):
        self.lbl.text = "       Пишите сюда: \n voronovnr_1@mail.ru"
        if self.image:
            self.gr.add_widget(self.img)
            self.image = False

    def build(self):
        self.bx = BoxLayout(orientation="vertical")
        self.gr = GridLayout(rows=1)
        self.lbl = Label(text=self.txt1,
                         font_size="30sp")
        self.img = Image(source="QR-email.png")

        self.gr.add_widget(self.lbl)
        self.bx.add_widget(self.gr)
        self.bx.add_widget(Button(text="Помощь",
                             bold=True,
                             font_size = "30sp",
                             background_color='#000080',
                             size_hint=(1, 0.5),
                             on_press=lambda x: self.error_event()
                             ))
        return self.bx


class MyApp(App):
    running = True

    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False


if __name__ == "__main__":
    try:
        MyApp().run()
    except ConnectionRefusedError:
        ErrorApp().run()
