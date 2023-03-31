# <<------------- Для тестирования запустите скрипт MainApp и пропишите "server" ---------->>
# <<---------------------- принимает рабочий стол --------------------->>
# <<---------------------- отправляет координаты мыши --------------------->>

import socket

import threading
import sys
from PIL import Image  # изображение

import pyautogui  # много назначений

from threading import Thread  # потоки

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QGridLayout,QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect

IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
PORT = 9999

print("STARTED")
print(f"IP-adress: {IP}")
print(f"PORT-connected: {PORT}")
sock = socket.socket()  # создаем сокет
sock.bind((IP, PORT))  # к серверу
sock.listen()
conn, addr = sock.accept()


class ClientTheard(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.ex = Server(addr, self.conn)
        threading.Thread.__init__(self)

    def run(self):
        for colls in range(threading.active_count()):
            for rows in range(threading.active_count()):
                self.ex.grid.addWidget(self.ex.label, colls, rows)


class WarningWindow(QDialog):
    def __init__(self, get_message):
        super().__init__()

        self.setWindowTitle("Warning")
        self.setGeometry(100, 100, 200, 200)

        label = QLabel(f"Внимание было закрыто {get_message}")

        # Создаем кнопку
        button = QPushButton("Закрыть")
        button.clicked.connect(self.close)

        # Создаем макет и добавляем метку и кнопку в макет
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        # Устанавливаем макет для диалогового окна
        self.setLayout(layout)

        self.exec_()


class Server(QMainWindow):
    def __init__(self, addr, conn):
        super().__init__()
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.grid = QGridLayout()
        self.addr = addr
        self.conn = conn
        self.initUI()
        self.mouse_x, self.mouse_y = map(int, pyautogui.position())

    def ChangeImage(self):
        not_habitat_programs = True
        try:
            while not_habitat_programs:
                data = conn.recv(999999)
                try:
                    message = data.decode()
                    if message[0] == "Z":
                        print("KIll")
                        # not_habitat_programs = False
                        # self.message_app(message[1:])
                except:
                    full = self.pixmap.loadFromData(data)
                    if full:
                        self.pixmap.loadFromData(data)
                        self.label.setScaledContents(True)
                        self.label.resize(self.width(), self.height())
                        self.label.setPixmap(self.pixmap)
        except ConnectionResetError:
            self.conn.close()

    def initUI(self):
        self.setWindowIcon(QIcon('image/logo-start.png'))  # лого основного окна
        self.label.resize(self.width(), self.height())  # задаем размеры Label
        x, y = map(int, pyautogui.size())  # размеры экрана
        self.setGeometry(QRect(x // 4, y // 4, x // 2, y // 2))  # окно проецирования
        self.setFixedSize(self.width(), self.height())
        self.setLayout(self.grid)
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.setWindowTitle(str(addr))  # имя окна
        self.start.start()

    def message_app(self, get_message):
        message_box = WarningWindow(get_message)


app = QApplication(sys.argv)
ex = Server(conn, addr)
ex.show()
sys.exit(app.exec_())
