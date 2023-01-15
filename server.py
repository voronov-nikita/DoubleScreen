# <<---------------------- принимает рабочий стол --------------------->>
# <<---------------------- отправляет координаты мыши --------------------->>

import socket
import threading

import mouse
from PIL import Image  # изображение

import pyautogui  # много назначений

from threading import Thread  # потоки

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect

IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
PORT = 9999

print("STARTED")
print(f"IP-adress: {IP}")
print(f"PORT-connected: {PORT}")
sock = socket.socket()  # создаем сокет
sock.bind((IP, PORT))  # к серверу


class ClientTheard(threading.Thread):
    def __init__(self, conn, grid):
        self.conn = conn
        self.grid = grid
        self.ex = Dekstop(self.conn, self.grid)
        threading.Thread.__init__(self)
        print("Подключился:", addr)

    def run(self):
        for colls in range(threading.active_count()):
            for rows in range(threading.active_count()):
                self.grid.addWidget(self.ex.label, colls, rows)


class Dekstop(QMainWindow):
    def __init__(self, conn, grid):
        super().__init__()
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.grid = grid
        self.conn = conn
        self.initUI()
        self.mouse_x, self.mouse_y = map(int, pyautogui.position())

    def ChangeImage(self):
        try:
            while True:
                data = self.conn.recv(999999)  # Принимаем данные с клиента
                full = self.pixmap.loadFromData(data)
                if full:
                    self.pixmap.loadFromData(data)
                    self.label.setScaledContents(True)
                    self.label.resize(self.width(), self.height())
                    self.label.setPixmap(self.pixmap)
                # self.mouse_control()
        except ConnectionResetError:
            QMessageBox.about(self, "   ERROR   ", "  Error    Client    ")
            self.conn.close()

    def initUI(self):
        self.setWindowIcon(QIcon('logo-start.png'))  # лого основного окна
        self.label.resize(self.width(), self.height())  # задаем размеры Label
        x, y = map(int, pyautogui.size())  # размеры экрана
        self.setGeometry(QRect(x // 4.5, y // 4.5, x // 1.5, y // 1.5))  # окно проецирования
        self.setFixedSize(self.width(), self.height())
        self.setLayout(self.grid)
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.setWindowTitle(str(addr))  # имя окна
        self.start.start()

    def mouse_control(self):
        mouse_x, mouse_y = map(int, pyautogui.position())  # считываем координа мыши
        self.conn.send(str(mouse_x).encode('utf-8'))  # отправляем координаты мыши по X
        self.conn.send(" ".encode('utf-8'))  # для разделения координат x/y
        self.conn.send(str(mouse_y).encode('utf-8'))  # отправляем координаты мыши по Y

        # <------------Нуждается в доработке------------>
        if mouse.is_pressed(button="left"):
            self.conn.send("LMouseClick".encode('utf-8'))
            self.conn.send(" ".encode('utf-8'))
        elif mouse.is_pressed(button="right"):
            self.conn.send("RMouseClick".encode('utf-8'))
            self.conn.send(" ".encode('utf-8'))
        else:
            mouse_x, mouse_y = map(int, pyautogui.position())  # считываем координа мыши
            self.conn.send(str(mouse_x).encode('utf-8'))  # отправляем координаты мыши по X
            self.conn.send(" ".encode('utf-8'))  # для разделения координат x/y
            self.conn.send(str(mouse_y).encode('utf-8'))  # отправляем координаты мыши по Y


if __name__ == '__main__':
    grid = QGridLayout()
    while True:
        sock.listen()  # слушвем сервер
        conn, addr = sock.accept()
        app = QApplication(sys.argv)
        ex = Dekstop(conn, grid)
        ex.show()  # показываем (транслируем) на экран
        sys.exit(app.exec())
