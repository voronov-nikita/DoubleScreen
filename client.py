# Приложение клиента для трансляции изображения
# Новео окно с двумя строками ввода и одной кнопкой
# НЕ ЗАКРЫВАТЬ! ПРОГРАММА СЛОМАЕТСЯ!
# Реализовать:
#
#
#

import socket

from PIL import ImageGrab
import io

from pyautogui import size
from psutil import process_iter

from threading import Thread
import time

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect

# глоабльные переменные
list_prohibited_programm = ["Telegram.exe"]


class AddInList(QDialog):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Введите название приложение и его формат:", self)

        self.line = QLineEdit(self)

        button = QPushButton("Сохранить", self)
        button.clicked.connect(self.save_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        layout.addWidget(button)

        # Устанавливаем макет для главного окна
        self.setLayout(layout)

    def save_data(self):
        text = self.line.text()
        if text not in list_prohibited_programm and text.split() != '':
            list_prohibited_programm.append(text)
        print(list_prohibited_programm)


class DekstopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.init_UI_Interact()

    def StartThread(self):
        self.start_change_image.start()
        self.start_process_find.start()

    def ChangeImage(self):
        try:
            if len(self.ip.text()) != 0 and len(self.port.text()):
                self.sock = socket.socket()
                self.sock.connect((self.ip.text(), int(self.port.text())))
                while True:
                    # <------------------Считывается и обрабатывается информация------------------>
                    img = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='JPEG',
                             optimize=True,
                             progressive=True)

                    # <------------------Отправка на Сервер------------------>
                    self.sock.send(img_bytes.getvalue())  # отправляем скриншот

        except ConnectionResetError:
            print(f"// DISCONNECT //")
            sys.exit()

    def ThreadProcessInfo(self):
        while True:
            # отслеживание активных процессов и невозможность открыть их
            for procces in process_iter():
                if procces.name() in list_prohibited_programm:
                    print("KILL:", procces.name())
                    self.sock.send(str("Z"+procces.name()).encode())
                    procces.kill()
                    break
            time.sleep(2)

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('image/logo-start.png'))  # лого окна приветствия
        self.label.resize(self.width(), self.height())  # задем размеры для Label
        x, y = map(int, size())  # размеры экрана

        self.setGeometry(QRect(x // 3, y // 3, 500, 110))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT")  # имя окна
        self.start_change_image = Thread(target=self.ChangeImage)
        self.start_process_find = Thread(target=self.ThreadProcessInfo)

        self.btn = QPushButton(self)  # кнопка
        self.btn.move(5, 55)
        self.btn.resize(470, 50)
        self.btn.clicked.connect(self.StartThread)
        self.btn.setText("Connected")  # текст кнопки

        self.ip = QLineEdit(self)  # IP-info
        self.ip.move(5, 5)  # положение линии ip
        self.ip.resize(470, 30)  # размеры линии ip
        self.ip.setPlaceholderText("IP-adress")

        self.port = QLineEdit(self)  # PORT- info
        self.port.move(5, 30)  # положение линии port
        self.port.resize(470, 30)  # размеры линии port
        self.port.setPlaceholderText("PORT-connect")

        self.settings = QPushButton(self)
        self.settings.move(470, 0)
        self.settings.resize(30, 30)
        self.btn.clicked.connect(self.add_new_habita_aplication)

    def add_new_habita_aplication(self):
        new_window = AddInList()
        new_window.exec_()


# это более выгодное решение с точки зрения открытия из нового файла
app = QApplication(sys.argv)
ex = DekstopApp()
ex.show()
sys.exit(app.exec())
