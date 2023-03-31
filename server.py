import socket

import threading
import sys

import pyautogui  # много назначений

from threading import Thread  # потоки

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QGridLayout, QVBoxLayout, QDialog
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


class WarningWindow(QDialog):
    def __init__(self, get_message):
        super().__init__()

        self.setWindowTitle("Warning")
        x, y = pyautogui.size()
        self.setGeometry(x // 2, y // 2, 200, 100)

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
        try:
            while True:
                data = conn.recv(999999)
                try:
                    message = data.decode()
                    if message[0] == "Z":
                        self.message_app(message[1:])
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
        sys.exit()


app = QApplication(sys.argv)
ex = Server(conn, addr)
ex.show()
sys.exit(app.exec_())
