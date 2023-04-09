import socket

import threading
import sys

import pyautogui  # много назначений

from threading import Thread  # потоки

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QShortcut, QVBoxLayout,\
    QDialog, QWidget, QAction
from PyQt5.QtGui import QPixmap, QIcon, QFont, QKeySequence
from PyQt5.QtCore import QRect, Qt

IP = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
PORT = 9999


class ClientTheard(threading.Thread):
    def __init__(self):
        self.ex = Server()
        threading.Thread.__init__(self)


class WarningWindow(QDialog):
    def __init__(self, get_message, name):
        super().__init__()

        self.setWindowTitle("Warning")
        x, y = pyautogui.size()
        self.setGeometry(x // 2, y // 2, 200, 100)

        label = QLabel(f"Внимание было закрыто: {get_message}\nПользователь: {name}")

        # Создаем кнопку
        button = QPushButton("Закрыть", self)
        button.clicked.connect(self.ok)

        # Создаем макет и добавляем метку и кнопку в макет
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        # Устанавливаем макет для диалогового окна
        self.setLayout(layout)
        self.setWindowIcon(QIcon('icologo.png'))

    def ok(self):
        self.close()


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Information")
        self.setWindowIcon(QIcon('icologo.png'))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        x, y = pyautogui.size()
        self.setGeometry(x // 2, y // 2, x // 5, y // 5)

        self.Init()

    def Init(self):
        x, y = pyautogui.size()

        self.label = QLabel(f"\t\tIP-aress: {IP}\n\t\tPORT-connected:{PORT}", self)
        self.label.move(5, 0)
        self.label.resize(x // 2, y // 9)

        button = QPushButton("Запустить", self)
        button.move(0, 90)
        button.resize(x // 5, y // 10)
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
        self.initAction()

        self.name_window = ""
        self.name_user = ""
        self.show_text = False
        self.list_color = ["#32CD32", "#8B0000", "#C71585", "#008080", "#FFD700", "#191970", "#FFFFFF", "#000000"]
        self.index_list_color = 0
        self.color = self.list_color[self.index_list_color]

        self.pixmap = QPixmap()
        self.label_image = QLabel(self)
        self.font_text = QFont()

        self.label_text1 = QLabel(self)
        self.label_text2 = QLabel(self)
        self.label_text3 = QLabel(self)

        self.initUI()

    def ChangeImage(self):
        try:
            while True:
                data = conn.recv(999999)
                try:
                    message = data.decode()
                    if message:
                        if message[0] == "N":
                            self.name_user = message[1:]
                        if message[0] == "Z":
                            self.message_app(message[1:], self.name_user)
                        if message[0] == "A" and message[1:] not in self.open_app:
                            self.open_app.append(message[1:])
                            print(message)

                except:
                    full = self.pixmap.loadFromData(data)
                    if full:
                        # обработка картинки
                        self.pixmap.loadFromData(data)
                        self.label_image.setScaledContents(True)
                        self.label_image.resize(self.width(), self.height())
                        self.label_image.setPixmap(self.pixmap)

                        # Обработка текста
                        self.show_text_label()

        except ConnectionResetError:
            self.conn.close()
            sys.exit(app.exec_())

    def initUI(self):
        self.setWindowIcon(QIcon('icologo.png'))  # лого основного окна
        self.label_image.resize(self.width(), self.height())

        kx, ky = 0.2, 0.1
        self.label_text1.resize(int(self.width() + self.width()*kx), int(self.height() - self.height()*ky))
        self.label_text2.resize(int(self.width() + self.width()*kx), int(self.height() - self.height()*ky))
        self.label_text3.resize(int(self.width() + self.width()*kx), int(self.height() - self.height()*ky))

        x, y = map(int, pyautogui.size())  # размеры экрана
        self.setGeometry(QRect(x // 4, y // 4, x // 2, y // 2))  # окно проецирования
        self.setFixedSize(self.width(), self.height())
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.setWindowTitle(f"{addr[0]} - {self.name_window}")  # имя окна
        self.start.start()

    def initAction(self):
        action1 = QAction("Выполнить", self)
        self.addAction(action1)
        action1.setShortcut(QKeySequence("Ctrl+Shift+H"))
        action1.triggered.connect(self.change_text_visibility)

        action2 = QAction("Выполнить", self)
        self.addAction(action2)
        action2.setShortcut(QKeySequence("Ctrl+Shift+C"))
        action2.triggered.connect(self.change_color_text)

    def message_app(self, get_message, name):
        message_box = WarningWindow(get_message, name)
        new_thread = Thread(target=message_box.exec_)
        new_thread.start()

    def change_text_visibility(self):
        self.show_text = (True, False)[self.show_text]

    def change_color_text(self):
        if self.index_list_color == len(self.list_color)-1:
            self.index_list_color = 0
        else:
            self.index_list_color += 1
        self.color = self.list_color[self.index_list_color]

    def show_text_label(self):
        if self.show_text:
            self.font_text.setPointSize(18)
            self.font_text.setBold(True)

            self.label_text1.setText(f"Открытые приложения")
            self.label_text1.setStyleSheet(f"color : {self.color}")
            self.label_text1.setFont(self.font_text)
            self.label_text1.setAlignment(Qt.AlignLeft)

            self.label_text2.setText(f"Имя: {self.name_user}")
            self.label_text2.setStyleSheet(f"color : {self.color}")
            self.label_text2.setFont(self.font_text)
            self.label_text2.setAlignment(Qt.AlignTop | Qt.AlignRight)

            self.label_text3.setText("Down Info")
            self.label_text3.setStyleSheet(f"color : {self.color}")
            self.label_text3.setFont(self.font_text)
            self.label_text3.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        else:
            self.label_text1.clear()
            self.label_text2.clear()
            self.label_text3.clear()


app = QApplication(sys.argv)
ex = InfoWindow()
ex.show()
sys.exit(app.exec_())
