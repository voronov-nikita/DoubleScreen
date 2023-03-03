# Приложение клиента для трансляции изображения
# Новео окно с двумя строками ввода и одной кнопкой
# НЕ ЗАКРЫВАТЬ! ПРОГРАММА СЛОМАЕТСЯ!
# Реализовать:
# 1) отслеживание открытия новых приложений
# 2)
#

import socket

from PIL import ImageGrab
import io

from pyautogui import size
from psutil import process_iter

from threading import Thread

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect

# глоабльные переменные
list_prohibited_programm = []


class DekstopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.init_UI_Interact()

    def StartThread(self):
        self.start.start()

    def ChangeImage(self):
        try:
            if len(self.ip.text()) != 0 and len(self.port.text()):
                sock = socket.socket()
                sock.connect((self.ip.text(), int(self.port.text())))
                while True:
                    # <------------------Считывается и обрабатывается информация------------------>
                    img = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='JPEG',
                             optimize=True,
                             progressive=True)

                    # <------------------Отправка на Сервер------------------>
                    sock.send(img_bytes.getvalue())  # отправляем скриншот

                    # отслеживание активных процессов и невозможность открыть их
                    for procces in process_iter():
                        if procces.name() in list_prohibited_programm:
                            print("KILL:", procces.name())
                            procces.kill()
                            break

        except ConnectionResetError:
            print("DISCONNECTED")

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('image/logo-start.png'))  # лого окна приветствия
        self.label.resize(self.width(), self.height())  # задем размеры для Label
        x, y = map(int, size())  # размеры экрана

        self.setGeometry(QRect(x // 3, y // 3, 500, 110))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT")  # имя окна
        self.start = Thread(target=self.ChangeImage)

        self.btn = QPushButton(self)  # кнопка
        self.btn.move(5, 55)
        self.btn.resize(470, 50)
        self.btn.clicked.connect(self.StartThread)
        self.btn.setText("Connected")  # текст кнопки

        self.ip = QLineEdit(self)  # IP-info
        self.ip.move(5, 5)  # положение линии ip
        self.ip.resize(470, 30)  # размеры линии ip
        self.ip.setPlaceholderText("IP-adress")

        self.port = QLineEdit(self)  # PORT- info
        self.port.move(5, 30)  # положение линии port
        self.port.resize(470, 30)  # размеры линии port
        self.port.setPlaceholderText("PORT-connect")

        self.settings = QPushButton(self)
        self.settings.move(470, 0)
        self.settings.resize(30, 30)
        self.settings.setIcon(QIcon("/image/settings_icon.png"))
        self.settings.clicked.connect(self.OpenSettingsWindow)

    def OpenSettingsWindow(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DekstopApp()
    ex.show()
    sys.exit(app.exec())
