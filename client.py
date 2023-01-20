# <<------------- Для тестирования запустите скрипт MainApp и пропишите "client" ---------->>
# <<---------------------- отправляет рабочий стол --------------------->>
# <<--------------------- принимает координаты мыши --------------------->>

import socket

# import keyboard - пока не потребуется
# import mouse
from PIL import ImageGrab
import io

import pyautogui

from threading import Thread

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QWidget, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect


class DekstopApp(QDialog):
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
                    img = ImageGrab.grab()  # считываем данные экрана
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG',)  # типо сжимать изображение не получается

                    # <------------------Отправка на Сервер------------------>
                    sock.send(img_bytes.getvalue())  # отправляем скриншот

        except ConnectionResetError:
            print("DISCONNECTED")

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('logo-start.png'))  # лого окна приветствия
        self.label.resize(self.width(), self.height())  # задем размеры для Label
        x, y = map(int, pyautogui.size())  # размеры экрана

        self.setGeometry(QRect(x // 3, y // 3, 500, 100))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT")  # имя окна
        self.start = Thread(target=self.ChangeImage, daemon=True)

        self.btn = QPushButton(self)  # кнопка
        self.btn.move(5, 55)
        self.btn.resize(490, 50)
        self.btn.clicked.connect(self.StartThread)
        self.btn.setText("Connected")  # текст кнопки

        self.ip = QLineEdit(self)  # IP-info
        self.ip.move(5, 5)  # положение линии ip
        self.ip.resize(490, 30)  # размеры линии ip
        self.ip.setPlaceholderText("IP-adress")

        self.port = QLineEdit(self)  # PORT- info
        self.port.move(5, 30)  # положение линии port
        self.port.resize(490, 30)  # размеры линии port
        self.port.setPlaceholderText("PORT-connect")


