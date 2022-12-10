import socket

from os import getlogin

from PIL import Image  # изображение
import io
import numpy as np
from random import randint
import pyautogui    #много назначений

from threading import Thread  # потоки

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999

print("STARTED")
print(IP)
print(PORT)
sock = socket.socket()
sock.bind((IP, PORT))  # к серверу
sock.listen(1)  # максимум одно подключение
conn, addr = sock.accept()


class Dekstop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def ChangeImage(self):
        try:
            print("[SERVER]: CONNECTED: {0}!".format(addr[0]))
            while True:
                img_bytes = conn.recv(9999999)
                self.pixmap.loadFromData(img_bytes)
                self.label.setScaledContents(True)
                self.label.resize(self.width(), self.height())
                self.label.setPixmap(self.pixmap)
        except ConnectionResetError:
            QMessageBox.about(self, "ERROR", "Error Client")
            conn.close()

    def init_UI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 800, 450))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("server" + str(randint(99999, 999999)))
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
