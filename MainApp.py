# <<------------- Этот код снова работает ------------->>
# Этот код требуется для того, чтобы не запускать одновременно код client.py или server.py
# В будущем, скорее всего, из этого кода сделется единый интерфейс приложения.
# На данный момент это единственный способ опробовать приложение


from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, QSize

import sys
from pyautogui import size


class Desktop(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.title_name = "Observer"
        self.app = app

        self.position_connect = 0
        self.position_upload = 0
        self.list_connect_image = ["image/new_upload.png", "image/dont_upload.png"]
        self.list_upload_image = ["image/Конект.png", "image/Disconnect.png"]

        self.InitUI()

    def InitUI(self):
        self.setWindowIcon(QIcon('image/logo-start.png'))  # лого основного окна
        x, y = map(int, size())  # размеры экрана
        self.setGeometry(QRect(x // 4, y // 4, x // 2, x // 4))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(self.title_name)  # имя окна

        self.btn1 = QPushButton(self)  # кнопка
        self.btn1.move(50, 50)
        self.btn1.resize(300, 300)
        self.btn1.clicked.connect(self.client_app)
        self.btn1.setIcon(QIcon(self.list_connect_image[self.position_connect]))
        self.btn1.setIconSize(QSize(300, 300))

        self.btn2 = QPushButton(self)  # кнопка
        self.btn2.move(450, 50)
        self.btn2.resize(300, 300)
        self.btn2.clicked.connect(self.server_app)
        self.btn2.setIcon(QIcon(self.list_upload_image[self.position_upload]))
        self.btn2.setIconSize(QSize(300, 300))

        self.btn_help = QPushButton(self)
        self.btn_help.move(x // 4, y // 4)
        self.btn_help.resize(30, 30)
        # self.btn2.clicked.connect(self.server_app)
        self.btn_help.setIcon(QIcon("image/help.png"))
        self.btn_help.setIconSize(QSize(30, 30))

    def client_app(self):
        import client
        # while True:
        # app = client.QApplication(client.sys.argv)
        self.position_connect -= 1
        self.btn1.setIcon(QIcon(self.list_connect_image[self.position_connect]))
        ex = client.DekstopApp()
        ex.show()  # показываем (транслируем) на экран
        # client.sys.exit(self.app.exec())

    def server_app(self):
        self.position_upload -= 1
        self.btn2.setIcon(QIcon(self.list_upload_image[self.position_upload]))
        import server
        # grid = server.QGridLayout()
        server.sock.listen()  # слушаем сервер
        conn, addr = server.sock.accept()
        ex = server.For_server(addr, conn)
        # server.sys.exit(self.app.exec())


if __name__ == "__main__":
    main_app = QApplication(sys.argv)
    cls = Desktop(main_app)
    cls.setObjectName("MainWindow")
    cls.setStyleSheet("#MainWindow{background-color:green}")
    cls.show()
    sys.exit(main_app.exec())
