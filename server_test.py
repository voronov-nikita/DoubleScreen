from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout


# Config.set("graphics", "relizeble", "0")# ---\
# Config.set("graphics", "width", "400")   #    \ высота и ширина экрана, изменять его потом нельзя
# Config.set("graphics", "heigth", "600")#------/

class MyApp(App):
    def build(self):
        fl = AnchorLayout()
        bl = BoxLayout(orientation="vertical", size_hint=(.5, .5))
        self.text_input = TextInput()
        bl.add_widget(self.text_input)  # позиция

        bl.add_widget(Button(
            text="Получить данные из TextInput",
            font_size=13,  # font_size рaзмер шрифта
            on_press=self.btn_press,  # on_press нажата
            background_color=[1, 0, 0, 1],  # background_color цвет RGBA в %
            background_normal="",  # background_normal  делает цвет ярче
        ))  # позиция

        fl.add_widget(bl)
        # s = Scatter()
        # s.add_widget(fl)
        return fl

    def on_text(self, instance, value):
        self.on_text.text = print(self.on_text)

    def btn_press(self, instance):
        print(self.text_input.text)


if __name__ == "__main__":
    MyApp().run()
