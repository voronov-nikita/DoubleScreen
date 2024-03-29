import socket

import pyautogui
from PIL import ImageGrab
import io

from pyautogui import size
from psutil import process_iter

from threading import Thread
import time

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect, Qt

# глоабльные переменные
list_prohibited_programm = []


class ViewList(QDialog):
    def __init__(self):
        super(ViewList, self).__init__()

        the_list = ('\n'.join(list_prohibited_programm), "Пусто")[len(list_prohibited_programm) == 0]

        self.label = QLabel(str(the_list), self)

        button = QPushButton("Закрыть", self)
        button.clicked.connect(self.close)
        button.setStyleSheet("""
        background: rgb(31, 31, 31);
        color: rgb(0, 47, 84);
        font-weight: bold;
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button)

        # Устанавливаем макет для главного окна
        self.setLayout(layout)
        x, y = size()
        self.setGeometry(x // 2, y // 2, 200, 100)
        self.setWindowIcon(QIcon('../icologo.png'))
        self.setWindowTitle("Добавить запрещенные программы")


class AddInList(QDialog):
    def __init__(self):
        super().__init__()


        self.line = QLineEdit(self)
        self.line.setPlaceholderText("Name and format")
        self.line.resize(300, 60)
        self.line.setStyleSheet("""
        background: rgb(40, 40, 40);
        color: rgb(0, 255, 175);
        border: 1px solid rgb(0, 200, 120);
        """)

        button_save = QPushButton("Сохранить", self)
        button_save.clicked.connect(self.save_data)
        button_save.move(0, 60)
        button_save.resize(300, 40)
        button_save.setStyleSheet("""
        background: rgb(40, 40, 40);
        color: rgb(0, 255, 175);
        border:0%;""")

        button_watch = QPushButton("Просмотреть список", self)
        button_watch.clicked.connect(self.watch_list_app)
        button_watch.move(0, 100)
        button_watch.resize(300, 40)
        button_watch.setStyleSheet("""
        background: rgb(40, 40, 40);
        color: rgb(0, 255, 175);
        border: dashed red;""")

        button_ready = QPushButton("Готово", self)
        button_ready.clicked.connect(self.close)
        button_ready.move(0, 140)
        button_ready.resize(300, 60)
        button_ready.setStyleSheet("""
        background: rgb(40, 40, 40);
        color: rgb(0, 255, 175);
        border:0%;""")

        self.setWindowIcon(QIcon('../icologo.png'))
        x, y = pyautogui.size()
        self.setGeometry(QRect(x//3, y//3, 300, 200))
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Добавить запрещенные программы")

    def save_data(self):
        text = self.line.text()
        if text not in list_prohibited_programm and text.split() != '':
            list_prohibited_programm.append(text.lower())
        self.line.clear()
        self.start_clear_programm()

    def watch_list_app(self):
        view_list = ViewList()
        view_list.exec_()

    def start_clear_programm(self):
        for procces in process_iter():
            if procces.name().lower() in list_prohibited_programm:
                procces.kill()


class DekstopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connected = True
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.add_new_habita_aplication()
        self.init_UI_Interact()

    def StartThread(self):
        self.start_change_image.start()
        self.start_process_find.start()

    def ChangeImage(self):
        try:
            if len(self.ip.text()) != 0 and len(self.port.text()):
                self.sock = socket.socket()
                self.sock.connect((self.ip.text(), int(self.port.text())))
                self.sock.send(str("N" + socket.gethostname()).encode())
                while self.connected:
                    # <------------------Считывается и обрабатывается информация------------------>
                    img = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG', optimize=True, )

                    # <------------------Отправка на Сервер------------------>
                    self.sock.send(img_bytes.getvalue())  # отправляем скриншот

        except ConnectionResetError:
            self.connected = False
            sys.exit(app.exec())

    def ThreadProcessInfo(self):
        while self.connected:
            # отслеживание активных процессов и невозможность открыть их
            for procces in process_iter():
                if procces.name().lower() in list_prohibited_programm:
                    self.sock.send(str("N" + str(socket.gethostname())).encode())
                    self.sock.send(str("Z" + procces.name()).encode())
                    procces.kill()
                    break
            time.sleep(2)

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('../icologo.png'))  # лого окна приветствия
        self.label.resize(self.width(), self.height())  # задем размеры для Label
        x, y = map(int, size())  # размеры экрана

        self.setGeometry(QRect(x // 3, y // 3, 500, 110))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT APP")  # имя окна
        self.start_change_image = Thread(target=self.ChangeImage)
        self.start_process_find = Thread(target=self.ThreadProcessInfo)

        self.btn = QPushButton(self)  # кнопка
        self.btn.move(0, 55)
        self.btn.resize(500, 55)
        self.btn.clicked.connect(self.StartThread)
        self.btn.setText("Connected")  # текст кнопки
        self.btn.setStyleSheet("""
        background: rgb(31, 31, 31);
        color: rgb(78, 201, 176);
        font-weight: bold;""")

        self.ip = QLineEdit(self)  # IP-info
        self.ip.move(0, 5)  # положение линии ip
        self.ip.resize(500, 30)  # размеры линии ip
        self.ip.setPlaceholderText("IP-adress")
        self.ip.setStyleSheet("""
        background: rgb(40, 40, 40);
        color: rgb(0, 255, 175);
        border:0%;""")

        self.port = QLineEdit(self)  # PORT- info
        self.port.move(0, 30)  # положение линии port
        self.port.resize(500, 30)  # размеры линии port
        self.port.setPlaceholderText("PORT-connect")
        self.port.setStyleSheet("""
        border: 0%;
        background: rgb(40, 40, 40);
        color: rgb(0, 255, 175);""")

    def add_new_habita_aplication(self):
        new_window = AddInList()
        new_window.exec_()


# это более выгодное решение с точки зрения открытия из нового файла
app = QApplication(sys.argv)
ex = DekstopApp()
ex.show()
sys.exit(app.exec())
