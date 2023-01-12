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
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect


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
                    img = ImageGrab.grab()  # считываем данные экрана
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='JPEG', optimize=True, progressive=True)  # типо НЕ сжимаем изображение

                    # <------------------Отправка на Сервер------------------>
                    sock.send(img_bytes.getvalue())  # отправляем скриншот
                    # sock.send(bytes(" "))

                    # <------------------Принимаем с Сервера------------------>
                    # k = 0
                    # rmouseclk = False  # обнуляем проверку на клик правой кнопкой
                    # lmouseclk = False  # обнуляем проверку на клик левой кнопкой
                    # data = sock.recv(99999999)  # Принимаем данные с сервера
                    # try:
                    #     if data.decode('utf-8'):  # проверка можно ли декодировать
                    #         # <-----------Проверить на получение нажатия----------->
                    #         if "R" in ''.join(data.decode('utf-8')):  # проверка нажатия правой кнопки мыши
                    #             rmouseclk = True
                    #         if "L" in ''.join(data.decode('utf-8')):  # проверка нажатия левой кнопкой мыши
                    #             lmouseclk = True
                    #
                    #         new_data = data.decode('utf-8').split()
                    #         print(new_data)
                    #         if k == 0:
                    #             self.mouse_x = int(new_data[0])  # задаем значение для X
                    #             k = 1
                    #         else:
                    #             self.mouse_y = int(new_data[-1])  # задаем значение для Y
                    #             k = 0
                    #             if rmouseclk:
                    #                 pyautogui.mouseDown(button='left')   # нажать на левую кнопку
                    #             if lmouseclk:
                    #                 pyautogui.mouseDown(button='right')  # нажать на правую кнопку
                    #
                    #             pyautogui.moveTo(self.mouse_x,
                    #                              self.mouse_y)  # для того, чтобы менять координаты мыши на то, что выдает клиент
                    #
                    #
                    # except UnicodeDecodeError:
                    #     print("Error decode")

        except ConnectionResetError:
            print("DISCONNECTED")

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('logo-start.png'))  # лого окна приветствия
        self.label.resize(self.width(), self.height())
        x, y = map(int, pyautogui.size())  # размеры экрана

        self.setGeometry(QRect(x // 3, y // 3, 500, 100))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT")
        self.start = Thread(target=self.ChangeImage, daemon=True)

        self.btn = QPushButton(self)
        self.btn.move(5, 55)
        self.btn.resize(490, 50)
        self.btn.clicked.connect(self.StartThread)
        self.btn.setText("Connected")  # текст кнопки

        self.ip = QLineEdit(self)  # IP-info
        self.ip.move(5, 5)
        self.ip.resize(490, 30)
        self.ip.setPlaceholderText("IP-adress")

        self.port = QLineEdit(self)  # PORT- info
        self.port.move(5, 30)
        self.port.resize(490, 30)
        self.port.setPlaceholderText("PORT-connect")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DekstopApp()
    ex.show()
    sys.exit(app.exec())
