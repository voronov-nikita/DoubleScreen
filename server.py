import socket

import threading
import sys

import pyautogui  # много назначений

from threading import Thread  # потоки

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QGridLayout, QVBoxLayout, QDialog, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect, Qt

IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
PORT = 9999


class ClientTheard(threading.Thread):
    def __init__(self):
        self.ex = Server()
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


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Information")
        self.setWindowIcon(QIcon('icologo.png'))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        x, y = pyautogui.size()
        self.setGeometry(x // 2, y // 2, x//5, y//5)

        self.Init()

    def Init(self):
        x, y = pyautogui.size()

        self.label = QLabel(f"\t\tIP-aress: {IP}\n\t\tPORT-connected:{PORT}", self)
        self.label.move(5, 0)
        self.label.resize(x//2, y//9)

        button = QPushButton("Запустить", self)
        button.move(0, 90)
        button.resize(x//5, y//10)
        button.clicked.connect(self.start_programm)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button)

    def start_programm(self):
        sock = socket.socket()  # создаем сокет
        sock.bind((IP, PORT))  # к серверу
        sock.listen()
        global conn, addr
        conn, addr = sock.accept()

        ex = Server()
        ex.show()
        self.close()


class Server(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.grid = QGridLayout()
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
        self.setWindowIcon(QIcon('icologo.png'))  # лого основного окна
        self.label.resize(self.width(), self.height())  # задаем размеры Label
        x, y = map(int, pyautogui.size())  # размеры экрана
        self.setGeometry(QRect(x // 4, y // 4, x // 2, y // 2))  # окно проецирования
        self.setFixedSize(self.width(), self.height())
        self.setLayout(self.grid)
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.setWindowTitle(str(addr[0]))  # имя окна
        self.start.start()

    def message_app(self, get_message):
        message_box = WarningWindow(get_message)
        sys.exit()


app = QApplication(sys.argv)
ex = InfoWindow()
ex.show()
sys.exit(app.exec_())
