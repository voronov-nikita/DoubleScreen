from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# Конфиг#

Config.set('graphics', 'widht', '640');
Config.set('graphics', 'height', '480');
Config.set('graphics', 'resizeable', '0');


# Оформление программы#

class MyApp(App):
    def build(self):
        btn = BoxLayout()
        textinput = TextInput
        # btn.add_widget(Button(text="Btn", on_press=self.on_text()))
        textinput.bind(text=self.on_text)
        self.var = btn.add_widget(TextInput(size_hint=(.5, .25)))
        return btn

    # Функции приложения#

    def on_text(instance,value):
        s=value
        print(s)


# Запуск#

if __name__ == "__main__":
    MyApp().run()