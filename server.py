import socket

from PIL import Image  # изображение

import pyautogui  # много назначений

from threading import Thread  # потоки

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect, Qt

IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
PORT = 9999

print("STARTED")
print(f"IP-adress: {IP}")
print(f"PORT-connected: {PORT}")
sock = socket.socket()  # создаем сокет
sock.bind((IP, PORT))  # к серверу
sock.listen()
conn, addr = sock.accept()


class Dekstop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mouse_x, self.mouse_y = map(int, pyautogui.position())

    def ChangeImage(self):
        try:
            while True:
                rmouseclk = False  # обнуляем проверку на клик правой кнопкой
                lmouseclk = False  # обнуляем проверку на клик левой кнопкой
                data = conn.recv(99999999)  # Принимаем данные с клиента
                try:
                    if data.decode('utf-8'):  # проверка можно ли декодировать

                        # <-----------Проверить на получение нажатия----------->
                        if data.decode('utf-8') == "RMouseClick":  # проверка нажатия правой кнопки мыши
                            rmouseclk = True
                        if data.decode('utf-8') == "LMouseClick":  # проверка нажатия левой кнопкой мыши
                            lmouseclk = True

                        self.mouse_x = int(data.decode('utf-8').split()[0])  # задаем значение для X
                        self.mouse_y = int(data.decode('utf-8').split()[1])  # задаем значение для Y

                except UnicodeDecodeError:
                    full = self.pixmap.loadFromData(data)
                    if full:
                        self.pixmap.loadFromData(data)
                        self.label.setScaledContents(True)
                        self.label.resize(self.width(), self.height())
                        self.label.setPixmap(self.pixmap)

                        # <----------------Требует доработки----------------->
                        ## if rmouseclk:
                        ##     pyautogui.mouseDown(button='left')   # нажать на левую кнопку
                        ## if lmouseclk:
                        ##     pyautogui.mouseDown(button='right')  # нажать на правую кнопку
                        # pyautogui.moveTo(self.mouse_x, self.mouse_y, 2)  # для того, чтобы менять координаты мыши на то, что выдает клиент


        except ConnectionResetError:
            QMessageBox.about(self, "ERROR", "Error Client")
            conn.close()

    def initUI(self):
        self.setWindowIcon(QIcon('logo-start.png'))  # лого основного окна
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        x, y = map(int, pyautogui.size())  # размеры экрана
        self.setGeometry(QRect(x // 4, y // 4, 800, 450))  # окно проецирования
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("server")
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
