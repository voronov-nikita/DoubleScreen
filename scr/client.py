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
list_prohibited_programm = []


class ViewList(QDialog):
    def __init__(self):
        super(ViewList, self).__init__()

        the_list = ('\n'.join(list_prohibited_programm), "Пусто")[len(list_prohibited_programm)==0]

        self.label = QLabel(str(the_list), self)

        button = QPushButton("Закрыть", self)
        button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button)

        # Устанавливаем макет для главного окна
        self.setLayout(layout)
        x, y = size()
        self.setGeometry(x // 2, y // 2, 200, 100)
        self.setWindowIcon(QIcon('icologo.png'))
        self.setWindowTitle("Добавить запрещенные программы")


class AddInList(QDialog):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Введите название приложение и его формат:", self)

        self.line = QLineEdit(self)

        button_save = QPushButton("Сохранить", self)
        button_save.clicked.connect(self.save_data)

        button_watch = QPushButton("Просмотреть список", self)
        button_watch.clicked.connect(self.watch_list_app)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        layout.addWidget(button_watch)
        layout.addWidget(button_save)

        # Устанавливаем макет для главного окна
        self.setLayout(layout)
        self.setWindowIcon(QIcon('icologo.png'))
        self.setWindowTitle("Добавить запрещенные программы")

    def save_data(self):
        text = self.line.text()
        if text not in list_prohibited_programm and text.split() != '':
            list_prohibited_programm.append(text)
        self.line.clear()

    def watch_list_app(self):
        view_list = ViewList()
        view_list.exec_()


class DekstopApp(QMainWindow):
    def __init__(self):
        super().__init__()
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
            # print(f"// DISCONNECT //")
            sys.exit()

    def ThreadProcessInfo(self):
        while True:
            # отслеживание активных процессов и невозможность открыть их
            for procces in process_iter():
                if procces.name() in list_prohibited_programm:
                    # print("KILL:", procces.name())
                    self.sock.send(str("Z" + procces.name()).encode())
                    procces.kill()
                    break
            time.sleep(2)

    def init_UI_Interact(self):
        self.setWindowIcon(QIcon('icologo.png'))  # лого окна приветствия
        self.label.resize(self.width(), self.height())  # задем размеры для Label
        x, y = map(int, size())  # размеры экрана

        self.setGeometry(QRect(x // 3, y // 3, 500, 110))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("CLIENT")  # имя окна
        self.start_change_image = Thread(target=self.ChangeImage)
        self.start_process_find = Thread(target=self.ThreadProcessInfo)

        self.btn = QPushButton(self)  # кнопка
        self.btn.move(5, 55)
        self.btn.resize(490, 50)
        self.btn.clicked.connect(self.StartThread)
        self.btn.setText("Connected")  # текст кнопки

        self.ip = QLineEdit(self)  # IP-info
        self.ip.move(5, 5)  # положение линии ip
        self.ip.resize(490, 30)  # размеры линии ip
        self.ip.setPlaceholderText("IP-adress")

        self.port = QLineEdit(self)  # PORT- info
        self.port.move(5, 30)  # положение линии port
        self.port.resize(490, 30)  # размеры линии port
        self.port.setPlaceholderText("PORT-connect")

    def add_new_habita_aplication(self):
        new_window = AddInList()
        new_window.exec_()


# это более выгодное решение с точки зрения открытия из нового файла
app = QApplication(sys.argv)
ex = DekstopApp()
ex.show()
sys.exit(app.exec())
