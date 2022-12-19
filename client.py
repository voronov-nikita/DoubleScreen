import socket

# import keyboard - пока не потребуется
import mouse
from PIL import ImageGrab
import io

import pyautogui

from threading import Thread

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect, Qt


class Dekstop(QMainWindow):
    def __init__(self):
        super().__init__()
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
                    img.save(img_bytes, format='PNG')

                    mouse_x, mouse_y = map(int, pyautogui.position())  # считываем координа мыши

                    # <------------------Отправка на Сервер------------------>
                    sock.send(img_bytes.getvalue())  # отправляем скриншот

                    sock.send(str(mouse_x).encode('utf-8'))  # отправляем координаты мыши по X
                    sock.send(" ".encode('utf-8'))  # для разделения координат x/y
                    sock.send(str(mouse_y).encode('utf-8'))  # отправляем координаты мыши по Y

                    # <------------Нуждается в доработке------------>
                    # if mouse.is_pressed(button="left"):
                    #     sock.send("LMouseClick".encode('utf-8'))
                    # if mouse.is_pressed(button="right"):
                    #     sock.send("RMouseClick".encode('utf-8'))
        except ConnectionResetError:
            print("DISCONNECTED")

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('logo-start.png'))  # лого окна приветствия
        self.pixmap = QPixmap()
        label = QLabel(self)
        label.resize(self.width(), self.height())
        x, y = map(int, pyautogui.size())  # размеры экрана
        self.setGeometry(QRect(x // 3, y // 3, 500, 100))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT")
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.btn = QPushButton(self)
        self.btn.move(5, 55)
        self.btn.resize(490, 50)
        self.btn.setText("Connect")
        self.btn.clicked.connect(self.StartThread)
        self.ip = QLineEdit(self)
        self.ip.move(5, 5)
        self.ip.resize(490, 30)
        self.ip.setPlaceholderText("IP-adress")
        self.port = QLineEdit(self)
        self.port.move(5, 30)
        self.port.resize(490, 30)
        self.port.setPlaceholderText("PORT-connect")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
