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
        self.InitUI()

    def InitUI(self):
        self.setWindowIcon(QIcon('image/logo-start.png'))  # лого основного окна
        x, y = map(int, size())  # размеры экрана
        self.setGeometry(QRect(x // 4, y // 4, x // 2, x // 4))  # окно-подключение
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(self.title_name)  # имя окна

        self.btn1 = QPushButton(self)  # кнопка
        self.btn1.move(100, 75)
        self.btn1.resize(250, 250)
        self.btn1.clicked.connect(self.client_app)
        self.btn1.setIcon(QIcon("image/new_upload.png"))
        self.btn1.setIconSize(QSize(250, 250))

        self.btn2 = QPushButton(self)  # кнопка
        self.btn2.move(500, 75)
        self.btn2.resize(250, 250)
        self.btn2.clicked.connect(self.server_app)
        self.btn2.setIcon(QIcon("image/Конект.png"))
        self.btn2.setIconSize(QSize(250, 250))

    def client_app(self):
        import client
        # while True:
            # app = client.QApplication(client.sys.argv)
        self.btn1.setIcon(QIcon("image/dont_upload.png"))
        ex = client.DekstopApp()
        ex.show()  # показываем (транслируем) на экран
        # client.sys.exit(self.app.exec())

    def server_app(self):
        import server
        grid = server.QGridLayout()
        while True:
            server.sock.listen()  # слушвем сервер
            conn, addr = server.sock.accept()
            ex = server.Dekstop(addr, conn, grid)
            ex.show()  # показываем (транслируем) на экран
            server.sys.exit(self.app.exec())


if __name__ == "__main__":
    main_app = QApplication(sys.argv)
    cls = Desktop(main_app)
    cls.show()
    sys.exit(main_app.exec())
